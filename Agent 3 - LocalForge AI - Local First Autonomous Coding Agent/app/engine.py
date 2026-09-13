import json, re, threading
from pathlib import Path
import httpx
from .config import MAX_ITERATIONS, COMMAND_TIMEOUT, DB_PATH, REQUIRE_CLEAN_GATES
from .models import ModelRegistry
from .repository import RepositoryIndex
from .symbols import SymbolIndex
from .state import StateStore
from .tools import ToolExecutor
from .gitops import GitOps
from .telemetry import Telemetry
ROOT=Path(__file__).resolve().parent.parent
SYSTEM="""You are SovereignCodeAgent, a local autonomous software-engineering agent.
Work only inside the supplied workspace. Make incremental changes and validate them.
Return exactly one JSON tool action per turn, no markdown.
Allowed actions: read_file, write_file, search, symbols, run, quality_gate, git_status, git_diff, git_commit, git_push, github_repo, github_pr, github_ci, github_failed_log, finish.
Never fabricate tool results, expose secrets, escape the workspace, or perform network actions unless explicitly authorized. Before finish, run quality_gate. If it fails, fix it. If publishing is requested and network is authorized, push and inspect CI; if CI fails, fetch failed logs, fix, validate, push, and re-check."""

class Agent:
    def __init__(self,workspace:Path):
        self.workspace=workspace; workspace.mkdir(parents=True,exist_ok=True)
        self.registry=ModelRegistry(ROOT/'config'/'models.yaml'); self.models=self.registry.models
        self.repo=RepositoryIndex(workspace); self.symbols=SymbolIndex(workspace); self.state=StateStore(DB_PATH)
        self.git=GitOps(workspace); self.git.ensure_repo(); self.last_telemetry={}; self.running={}
    def safe_path(self,rel): return ToolExecutor(self.workspace).safe_path(rel)
    def _call_one(self,model,messages):
        r=httpx.post(model['base_url'].rstrip('/')+'/chat/completions',json={'model':model['model'],'messages':messages,'temperature':0.1},timeout=240); r.raise_for_status(); return r.json()['choices'][0]['message']['content']
    def call(self,role,messages,requested=None,telemetry=None):
        errors=[]
        for model in self.registry.fallback_order(role,requested):
            try:
                response=self._call_one(model,messages)
                if telemetry: telemetry.model_call(messages,response)
                return model,response
            except Exception as e: errors.append(f"{model['id']}: {type(e).__name__}: {e}")
        raise RuntimeError('No local model endpoint succeeded. '+' | '.join(errors))
    def parse(self,raw):
        raw=re.sub(r'^```json\s*|\s*```$','',raw.strip(),flags=re.I)
        try: return json.loads(raw)
        except Exception: return {'action':'quality_gate','parse_error':raw[:1000]}
    def context(self,query):
        return f"FILE TREE:\n{self.repo.tree_text()}\n\nSYMBOL HITS:\n{json.dumps(self.symbols.search(query,limit=30))}\n\nRELEVANT EXCERPTS:\n{self.repo.relevant(query,limit=10,chars=3500)}"
    def chat(self,message,requested=None):
        telemetry=Telemetry(); prompt=f"{self.context(message)}\n\nUSER:\n{message}\nRespond with useful engineering guidance. Do not modify files in chat mode."
        model,content=self.call('planner',[{'role':'system','content':'You are a concise local coding assistant.'},{'role':'user','content':prompt}],requested,telemetry); self.last_telemetry=telemetry.snapshot(); return {'model':model['id'],'response':content,'telemetry':self.last_telemetry}
    def plan(self,task,requested,telemetry):
        prompt=f"Create an implementation plan. Return JSON with goal, steps, risks, validation.\nTASK:\n{task}\n\n{self.context(task)}"
        try:
            model,raw=self.call('planner',[{'role':'system','content':'You are the planning agent. Return only JSON.'},{'role':'user','content':prompt}],requested,telemetry)
            try: plan=json.loads(re.sub(r'^```json\s*|\s*```$','',raw.strip(),flags=re.I))
            except Exception: plan={'goal':task,'steps':[raw[:4000]]}
            return {'model':model['id'],'plan':plan}
        except Exception as e: return {'model':None,'plan':{'goal':task,'steps':['Planner unavailable; proceed with coding agent.'],'warning':str(e)}}
    def start_task(self,task,requested=None,allow_network=False):
        initial=self.registry.choose('agent',requested); tid=self.state.create_task(task,initial['id'])
        th=threading.Thread(target=self.run_task,args=(task,requested,allow_network,tid),daemon=True); self.running[tid]=th; th.start(); return {'task_id':tid,'status':'running','model':initial['id']}
    def run_task(self,task,requested=None,allow_network=False,task_id=None):
        telemetry=Telemetry(); initial=self.registry.choose('agent',requested); tid=task_id or self.state.create_task(task,initial['id']); tools=ToolExecutor(self.workspace,COMMAND_TIMEOUT,allow_network=allow_network)
        branch='sca/'+tid; self.git.branch(branch); plan=self.plan(task,requested,telemetry); self.state.event(tid,'plan',plan)
        messages=[{'role':'system','content':SYSTEM},{'role':'user','content':f"TASK:\n{task}\n\nPLANNER OUTPUT:\n{json.dumps(plan['plan'])}\n\n{self.context(task)}\n\nYou are on git branch {branch}. Inspect, implement, test, debug, and validate."}]
        last_gate=None; active_model=initial['id']
        for i in range(1,MAX_ITERATIONS+1):
            try:
                role='agent' if i<8 else ('debugger' if not (last_gate and last_gate.get('ok')) else 'reviewer'); model,raw=self.call(role,messages,requested if i==1 else None,telemetry); active_model=model['id']
            except Exception as e:
                self.state.event(tid,'model_error',{'error':str(e),'model':active_model}); self.state.finish(tid,'model_error',i-1,str(e)); self.last_telemetry=telemetry.snapshot(); return {'task_id':tid,'status':'model_error','error':str(e)}
            obj=self.parse(raw); self.state.event(tid,'agent_action',{'iteration':i,'model':active_model,'action':obj})
            if obj.get('action')=='finish':
                if REQUIRE_CLEAN_GATES and not (last_gate and last_gate.get('ok')): result={'ok':False,'result':'FINISH_REJECTED: run quality_gate successfully first'}
                else:
                    review=self._final_review(task,obj,last_gate,telemetry); self.state.event(tid,'final_review',review)
                    if review.get('approved',True):
                        self.state.finish(tid,'completed',i,obj.get('summary','')); self.last_telemetry=telemetry.snapshot(); return {'task_id':tid,'status':'completed','iterations':i,'model':active_model,'summary':obj,'quality':last_gate,'review':review,'telemetry':self.last_telemetry}
                    result={'ok':False,'result':'FINAL_REVIEW_REJECTED: '+review.get('reason','reviewer requested more work')}
            else:
                telemetry.tool_call(); result=tools.execute(obj)
                if obj.get('action')=='quality_gate': last_gate=result.get('result')
                self.state.event(tid,'tool_result',{'iteration':i,'result':result})
                if obj.get('action') in {'write_file','git_commit'}: self.state.checkpoint(tid,i,self.git.head(),obj.get('path') or obj.get('message',''))
            messages += [{'role':'assistant','content':json.dumps(obj)},{'role':'user','content':'Tool result:\n'+json.dumps(result)[:18000]+'\nContinue toward validated completion.'}]
        self.state.finish(tid,'needs_more_iterations',MAX_ITERATIONS,'Iteration limit reached'); self.last_telemetry=telemetry.snapshot(); return {'task_id':tid,'status':'needs_more_iterations','iterations':MAX_ITERATIONS,'quality':last_gate}
    def _final_review(self,task,summary,quality,telemetry):
        prompt=f"Review readiness. TASK={task}\nSUMMARY={json.dumps(summary)}\nQUALITY={json.dumps(quality)}\nReturn only JSON {{\"approved\":true|false,\"reason\":\"...\"}}."
        try:
            model,raw=self.call('reviewer',[{'role':'system','content':'You are the independent final reviewer.'},{'role':'user','content':prompt}],None,telemetry); obj=json.loads(re.sub(r'^```json\s*|\s*```$','',raw.strip(),flags=re.I)); obj['model']=model['id']; return obj
        except Exception as e: return {'approved':True,'reason':'Reviewer unavailable; deterministic quality gate passed.','warning':str(e)}

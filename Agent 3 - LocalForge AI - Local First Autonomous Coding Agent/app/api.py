import asyncio, json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from .config import WORKSPACE
from .engine import Agent
from .quality import QualityGate
from .security import scan_secrets
from .symbols import SymbolIndex
from .githubops import GitHubOps
from .tools import ToolExecutor
router=APIRouter(); WORKSPACE.mkdir(parents=True,exist_ok=True); agent=Agent(WORKSPACE)
class ChatRequest(BaseModel): message:str; model:str|None=None; allow_network:bool=False
class WriteRequest(BaseModel): path:str; content:str
class TerminalRequest(BaseModel): command:str; allow_network:bool=False

def walk(p):
    out=[]
    for x in sorted(p.iterdir(),key=lambda z:(z.is_file(),z.name.lower())):
        if x.name in {'.git','.venv','node_modules','__pycache__','.sca'}: continue
        item={'name':x.name,'path':str(x.relative_to(WORKSPACE)).replace('\\','/'),'type':'file' if x.is_file() else 'dir'}
        if x.is_dir(): item['children']=walk(x)
        out.append(item)
    return out
@router.get('/tree')
def tree(): return {'workspace':str(WORKSPACE),'tree':walk(WORKSPACE)}
@router.get('/file')
def read_file(path:str):
    try: p=agent.safe_path(path)
    except ValueError as e: raise HTTPException(400,str(e))
    if not p.is_file(): raise HTTPException(404,'File not found')
    return {'path':path,'content':p.read_text(encoding='utf-8',errors='replace')}
@router.post('/file')
def write_file(req:WriteRequest):
    p=agent.safe_path(req.path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(req.content,encoding='utf-8'); return {'ok':True}
@router.get('/models')
def models(): return agent.models
@router.get('/models/health')
def model_health(): return agent.registry.health()
@router.post('/chat')
def chat(req:ChatRequest): return agent.chat(req.message,req.model)
@router.post('/task')
def task(req:ChatRequest): return agent.run_task(req.message,req.model,req.allow_network)
@router.post('/task/start')
def task_start(req:ChatRequest): return agent.start_task(req.message,req.model,req.allow_network)
@router.get('/tasks')
def tasks(): return agent.state.tasks()
@router.get('/tasks/{task_id}')
def task_detail(task_id:str):
    t=agent.state.task(task_id)
    if not t: raise HTTPException(404,'Task not found')
    return t
@router.get('/tasks/{task_id}/events')
def task_events(task_id:str,after:int=0): return {'events':agent.state.events_since(task_id,after)}
@router.get('/tasks/{task_id}/stream')
async def task_stream(task_id:str):
    if not agent.state.task(task_id): raise HTTPException(404,'Task not found')
    async def gen():
        last=0
        while True:
            for e in agent.state.events_since(task_id,last):
                last=e['id']; yield f"id: {last}\nevent: {e['kind']}\ndata: {json.dumps(e,ensure_ascii=False)}\n\n"
            t=agent.state.task(task_id)
            if t and t['status']!='running': yield f"event: done\ndata: {json.dumps({'status':t['status'],'task_id':task_id})}\n\n"; break
            await asyncio.sleep(.7)
    return StreamingResponse(gen(),media_type='text/event-stream',headers={'Cache-Control':'no-cache'})
@router.get('/quality')
def quality(): return QualityGate(WORKSPACE).run()
@router.get('/security')
def security(): return {'findings':scan_secrets(WORKSPACE)}
@router.get('/git/status')
def git_status(): return agent.git.status()
@router.get('/git/diff')
def git_diff(): return agent.git.diff()
@router.post('/terminal')
def terminal(req:TerminalRequest): return ToolExecutor(WORKSPACE,allow_network=req.allow_network).run(req.command)
@router.get('/symbols')
def symbols(query:str=''): return {'symbols':SymbolIndex(WORKSPACE).search(query)}
@router.get('/telemetry')
def telemetry(): return agent.last_telemetry
@router.get('/github/status')
def github_status():
    g=GitHubOps(WORKSPACE); return {'available':g.available(),'status':g.status() if g.available() else {'code':127,'stderr':'gh not installed','stdout':''}}

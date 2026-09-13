from pathlib import Path
from .gitops import GitOps
from .githubops import GitHubOps
from .quality import QualityGate
from .repository import RepositoryIndex
from .symbols import SymbolIndex
from .sandbox import SandboxRunner
BLOCKED_SUBSTRINGS=['rm -rf','format c:','del /s','shutdown','reboot','mkfs','dd if=','curl ','wget ','powershell -enc']
NETWORKY=['git push','gh repo create','gh pr create','npm publish','twine upload']
class ToolExecutor:
    def __init__(self,root:Path,timeout=180,allow_network=False):
        self.root=root; self.timeout=timeout; self.allow_network=allow_network; self.git=GitOps(root); self.github=GitHubOps(root); self.repo=RepositoryIndex(root); self.symbols=SymbolIndex(root); self.quality=QualityGate(root,timeout); self.sandbox=SandboxRunner(root,timeout)
    def safe_path(self,rel):
        p=(self.root/rel).resolve()
        if p!=self.root and self.root not in p.parents: raise ValueError('Path escapes workspace')
        return p
    def execute(self,obj):
        a=obj.get('action')
        if a=='write_file':
            p=self.safe_path(obj['path']); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(obj.get('content',''),encoding='utf-8'); return {'ok':True,'result':'WRITE_OK'}
        if a=='read_file': return {'ok':True,'result':self.safe_path(obj['path']).read_text(encoding='utf-8',errors='replace')[:50000]}
        if a=='search': return {'ok':True,'result':self.repo.search(obj.get('pattern',''))}
        if a=='symbols': return {'ok':True,'result':self.symbols.search(obj.get('query',''))}
        if a=='run': return self.run(obj.get('command',''))
        if a=='quality_gate':
            q=self.quality.run(); return {'ok':q['ok'],'result':q}
        if a=='git_status': return {'ok':True,'result':self.git.status()}
        if a=='git_diff': return {'ok':True,'result':self.git.diff()}
        if a=='git_commit': return {'ok':True,'result':self.git.commit(obj.get('message','SovereignCodeAgent changes'))}
        if a=='git_push':
            if not self.allow_network: return {'ok':False,'result':'NETWORK_APPROVAL_REQUIRED'}
            return {'ok':True,'result':self.git.push(obj.get('remote','origin'),obj.get('branch','HEAD'))}
        if a=='github_repo':
            if not self.allow_network: return {'ok':False,'result':'NETWORK_APPROVAL_REQUIRED'}
            r=self.github.create_repo(obj.get('name','sovereign-generated-app'),bool(obj.get('private',False))); return {'ok':r['code']==0,'result':r}
        if a=='github_pr':
            if not self.allow_network: return {'ok':False,'result':'NETWORK_APPROVAL_REQUIRED'}
            r=self.github.create_pr(obj.get('title','SovereignCodeAgent changes'),obj.get('body','Autonomous changes prepared by SovereignCodeAgent.')); return {'ok':r['code']==0,'result':r}
        if a=='github_ci':
            if not self.allow_network: return {'ok':False,'result':'NETWORK_APPROVAL_REQUIRED'}
            r=self.github.ci(); return {'ok':r['code']==0,'result':r}
        if a=='github_failed_log':
            if not self.allow_network: return {'ok':False,'result':'NETWORK_APPROVAL_REQUIRED'}
            r=self.github.view_failed(obj.get('run_id')); return {'ok':r['code']==0,'result':r}
        return {'ok':False,'result':'UNKNOWN_ACTION'}
    def run(self,command):
        low=command.lower()
        if any(x in low for x in BLOCKED_SUBSTRINGS): return {'ok':False,'result':'BLOCKED_UNSAFE_COMMAND'}
        if any(x in low for x in NETWORKY) and not self.allow_network: return {'ok':False,'result':'NETWORK_APPROVAL_REQUIRED'}
        return self.sandbox.run(command)

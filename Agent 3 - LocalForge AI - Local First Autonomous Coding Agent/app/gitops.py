import subprocess
from pathlib import Path
class GitOps:
    def __init__(self,root:Path): self.root=root
    def _run(self,*args):
        r=subprocess.run(['git',*args],cwd=self.root,text=True,capture_output=True,timeout=60); return {'code':r.returncode,'stdout':r.stdout.strip(),'stderr':r.stderr.strip()}
    def ensure_repo(self): return self._run('init') if not (self.root/'.git').exists() else {'code':0,'stdout':'already initialized','stderr':''}
    def status(self): return self._run('status','--short')
    def diff(self,cached=False): return self._run('diff',*(['--cached'] if cached else []))
    def diff_stat(self): return self._run('diff','--stat')
    def head(self):
        r=self._run('rev-parse','HEAD'); return r['stdout'] if r['code']==0 else ''
    def current_branch(self):
        r=self._run('branch','--show-current'); return r['stdout'] if r['code']==0 else ''
    def branch(self,name): return self._run('checkout','-B',name)
    def commit(self,message): self._run('add','-A'); return self._run('commit','-m',message)
    def push(self,remote='origin',branch='HEAD'): return self._run('push','-u',remote,branch)

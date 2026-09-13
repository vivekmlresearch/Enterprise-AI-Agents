import shutil, subprocess
from pathlib import Path

class GitHubOps:
    def __init__(self, root: Path): self.root=root
    def available(self): return shutil.which('gh') is not None
    def _run(self,*args,timeout=120):
        if not self.available(): return {'code':127,'stdout':'','stderr':'GitHub CLI (gh) is not installed'}
        r=subprocess.run(['gh',*args],cwd=self.root,text=True,capture_output=True,timeout=timeout)
        return {'code':r.returncode,'stdout':r.stdout.strip(),'stderr':r.stderr.strip()}
    def status(self): return self._run('auth','status')
    def create_repo(self,name,private=False):
        args=['repo','create',name,'--source=.','--remote=origin','--push']
        args += ['--private' if private else '--public']
        return self._run(*args,timeout=180)
    def create_pr(self,title,body='Autonomous changes prepared by SovereignCodeAgent.'):
        return self._run('pr','create','--title',title,'--body',body,timeout=180)
    def ci(self):
        return self._run('run','list','--limit','10','--json','databaseId,status,conclusion,workflowName,headBranch,url')
    def view_failed(self, run_id):
        return self._run('run','view',str(run_id),'--log-failed',timeout=180)

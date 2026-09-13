import shutil, subprocess
from pathlib import Path
from .config import USE_DOCKER_SANDBOX, SANDBOX_IMAGE

class SandboxRunner:
    def __init__(self, root: Path, timeout=180):
        self.root=root; self.timeout=timeout
    def docker_available(self): return shutil.which('docker') is not None
    def run(self, command):
        if USE_DOCKER_SANDBOX:
            if not self.docker_available(): return {'ok':False,'result':'DOCKER_SANDBOX_ENABLED_BUT_DOCKER_UNAVAILABLE'}
            args=['docker','run','--rm','--network','none','--cpus','2','--memory','4g','-v',f'{self.root}:/workspace','-w','/workspace',SANDBOX_IMAGE,'bash','-lc',command]
            try: r=subprocess.run(args,text=True,capture_output=True,timeout=self.timeout)
            except subprocess.TimeoutExpired: return {'ok':False,'result':'COMMAND_TIMEOUT'}
        else:
            try: r=subprocess.run(command,shell=True,cwd=self.root,text=True,capture_output=True,timeout=self.timeout)
            except subprocess.TimeoutExpired: return {'ok':False,'result':'COMMAND_TIMEOUT'}
        return {'ok':r.returncode==0,'result':f'exit={r.returncode}\nSTDOUT:\n{r.stdout[-16000:]}\nSTDERR:\n{r.stderr[-16000:]}'}

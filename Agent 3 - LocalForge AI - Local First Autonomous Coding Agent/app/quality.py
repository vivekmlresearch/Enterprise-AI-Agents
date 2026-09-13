import subprocess
from pathlib import Path
from .security import scan_secrets

class QualityGate:
    def __init__(self, root: Path, timeout=180): self.root=root; self.timeout=timeout
    def _cmd(self, command):
        try:
            r=subprocess.run(command,shell=True,cwd=self.root,text=True,capture_output=True,timeout=self.timeout)
            return {'command':command,'code':r.returncode,'stdout':r.stdout[-8000:],'stderr':r.stderr[-8000:]}
        except subprocess.TimeoutExpired:
            return {'command':command,'code':124,'stdout':'','stderr':'timeout'}
    def detect_checks(self):
        checks=[]
        if any(self.root.rglob('*.py')):
            checks += ['python -m compileall -q .']
            if (self.root/'tests').exists(): checks += ['pytest -q']
        if (self.root/'package.json').exists():
            txt=(self.root/'package.json').read_text(errors='ignore')
            if '"test"' in txt: checks += ['npm test -- --runInBand']
            if '"build"' in txt: checks += ['npm run build']
        return list(dict.fromkeys(checks))
    def run(self):
        results=[self._cmd(c) for c in self.detect_checks()]
        secrets=scan_secrets(self.root)
        return {'ok':all(r['code']==0 for r in results) and not secrets,'checks':results,'secrets':secrets}

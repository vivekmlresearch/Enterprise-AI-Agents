from pathlib import Path
from app.gitops import GitOps
from app.sandbox import SandboxRunner
from app.state import StateStore

def test_events_since(tmp_path):
    s=StateStore(tmp_path/'state.db'); tid=s.create_task('x','m'); s.event(tid,'plan',{'a':1}); s.event(tid,'tool_result',{'b':2})
    first=s.events_since(tid,0); assert len(first)==2; assert s.events_since(tid,first[0]['id'])[0]['kind']=='tool_result'

def test_git_diff(tmp_path):
    g=GitOps(tmp_path); assert g.ensure_repo()['code']==0
    (tmp_path/'a.txt').write_text('a')
    assert g.status()['code']==0

def test_sandbox_local(tmp_path):
    r=SandboxRunner(tmp_path,10).run('python -c "print(123)"')
    assert r['ok'] and '123' in r['result']

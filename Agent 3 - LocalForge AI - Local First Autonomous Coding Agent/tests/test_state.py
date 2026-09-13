from app.state import StateStore
def test_task_state(tmp_path):
    s=StateStore(tmp_path/'state.db'); tid=s.create_task('hello','phi-4'); s.event(tid,'x',{'a':1}); s.finish(tid,'completed',1,'ok')
    t=s.task(tid); assert t['status']=='completed' and t['events'][0]['payload']['a']==1

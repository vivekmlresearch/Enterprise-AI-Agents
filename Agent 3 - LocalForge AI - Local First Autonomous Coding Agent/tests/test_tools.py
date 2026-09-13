from app.tools import ToolExecutor
def test_path_escape_blocked(tmp_path):
    t=ToolExecutor(tmp_path)
    try: t.safe_path('../outside')
    except ValueError: pass
    else: raise AssertionError('escape was not blocked')
def test_unsafe_command_blocked(tmp_path):
    assert not ToolExecutor(tmp_path).run('rm -rf /')['ok']

from app.repository import RepositoryIndex
def test_relevant(tmp_path):
    (tmp_path/'alpha.py').write_text('def quantum_solver(): pass')
    (tmp_path/'beta.py').write_text('def other(): pass')
    assert 'alpha.py' in RepositoryIndex(tmp_path).relevant('quantum solver')

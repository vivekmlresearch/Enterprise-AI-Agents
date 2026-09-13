from app.security import scan_secrets
def test_secret_scan(tmp_path):
    (tmp_path/'x.py').write_text('TOKEN="ghp_abcdefghijklmnopqrstuvwxyz1234567890"')
    assert scan_secrets(tmp_path)

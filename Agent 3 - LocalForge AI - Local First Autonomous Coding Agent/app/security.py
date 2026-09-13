from pathlib import Path
import re

SECRET_PATTERNS={
 'private_key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
 'aws_access_key': re.compile(r'AKIA[0-9A-Z]{16}'),
 'github_token': re.compile(r'gh[pousr]_[A-Za-z0-9_]{30,}'),
 'generic_secret': re.compile(r'(?i)(api[_-]?key|secret|password)\s*[=:]\s*["\'][^"\']{8,}["\']'),
}
SKIP={'.git','.venv','node_modules','__pycache__'}

def scan_secrets(root: Path):
    findings=[]
    for p in root.rglob('*'):
        if not p.is_file() or any(x in SKIP for x in p.parts): continue
        try:
            if p.stat().st_size > 2_000_000: continue
            txt=p.read_text(encoding='utf-8',errors='ignore')
        except Exception: continue
        for name,rx in SECRET_PATTERNS.items():
            for m in rx.finditer(txt):
                line=txt.count('\\n',0,m.start())+1
                findings.append({'rule':name,'file':str(p.relative_to(root)),'line':line})
    return findings

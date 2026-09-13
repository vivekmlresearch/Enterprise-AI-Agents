from pathlib import Path
import re, subprocess

IGNORED={'.git','.venv','venv','node_modules','__pycache__','.pytest_cache','.mypy_cache','dist','build'}
TEXT_EXT={'.py','.js','.ts','.tsx','.jsx','.json','.yaml','.yml','.toml','.md','.txt','.html','.css','.scss','.sql','.sh','.ps1','.java','.go','.rs','.cpp','.c','.h','.hpp'}

class RepositoryIndex:
    def __init__(self, root: Path): self.root=root
    def files(self, limit=3000):
        rows=[]
        for p in self.root.rglob('*'):
            if len(rows)>=limit: break
            if p.is_file() and not any(x in IGNORED for x in p.parts):
                rows.append(str(p.relative_to(self.root)))
        return sorted(rows)
    def tree_text(self, limit=600): return '\n'.join(self.files(limit))
    def relevant(self, query: str, limit=12, chars=5000):
        terms=[x.lower() for x in re.findall(r'[A-Za-z_][A-Za-z0-9_]{2,}',query) if len(x)>2]
        scored=[]
        for rel in self.files():
            p=self.root/rel
            if p.suffix.lower() not in TEXT_EXT: continue
            try: txt=p.read_text(encoding='utf-8',errors='replace')[:60000]
            except Exception: continue
            low=(rel+'\n'+txt).lower()
            score=sum(low.count(t) for t in set(terms))
            if score: scored.append((score,rel,txt))
        scored.sort(reverse=True)
        return '\n\n'.join(f'### {rel} (score={score})\n{txt[:chars]}' for score,rel,txt in scored[:limit])
    def search(self, pattern: str, limit=100):
        try:
            r=subprocess.run(['git','grep','-n','-I','--',pattern],cwd=self.root,text=True,capture_output=True,timeout=30)
            return r.stdout.splitlines()[:limit]
        except Exception: return []

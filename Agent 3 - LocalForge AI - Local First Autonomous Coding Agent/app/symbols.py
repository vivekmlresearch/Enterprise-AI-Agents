import ast, re
from pathlib import Path
from .repository import IGNORED

class SymbolIndex:
    def __init__(self, root: Path): self.root=root
    def build(self, limit=5000):
        out=[]
        for p in self.root.rglob('*'):
            if len(out)>=limit: break
            if not p.is_file() or any(x in IGNORED for x in p.parts): continue
            rel=str(p.relative_to(self.root))
            if p.suffix=='.py':
                try:
                    tree=ast.parse(p.read_text(encoding='utf-8',errors='replace'))
                    for n in ast.walk(tree):
                        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                            out.append({'file':rel,'name':n.name,'kind':'class' if isinstance(n,ast.ClassDef) else 'function','line':getattr(n,'lineno',0)})
                except Exception: pass
            elif p.suffix.lower() in {'.js','.jsx','.ts','.tsx'}:
                try: txt=p.read_text(encoding='utf-8',errors='replace')
                except Exception: continue
                for m in re.finditer(r'(?m)^\s*(?:export\s+)?(?:async\s+)?(?:function|class)\s+([A-Za-z_$][\w$]*)',txt):
                    out.append({'file':rel,'name':m.group(1),'kind':'symbol','line':txt.count('\n',0,m.start())+1})
        return out
    def search(self, query, limit=50):
        q=query.lower()
        return [x for x in self.build() if q in x['name'].lower() or q in x['file'].lower()][:limit]

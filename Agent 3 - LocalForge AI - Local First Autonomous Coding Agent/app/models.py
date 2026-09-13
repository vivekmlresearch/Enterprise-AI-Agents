from pathlib import Path
import httpx, yaml

class ModelRegistry:
    def __init__(self, config: Path): self.config=config; self.models=self.load()
    def load(self): return yaml.safe_load(self.config.read_text(encoding='utf-8')).get('models',[])
    def get(self, id): return next((m for m in self.models if m['id']==id),None)
    def candidates(self, role): return sorted([m for m in self.models if role in m.get('roles',[])],key=lambda m:m.get('priority',99))
    def choose(self, role, requested=None):
        if requested and self.get(requested): return self.get(requested)
        xs=self.candidates(role); return xs[0] if xs else self.models[0]
    def fallback_order(self, role, requested=None):
        chosen=self.choose(role,requested); rest=[m for m in self.candidates(role) if m['id']!=chosen['id']]
        for m in self.models:
            if m['id']!=chosen['id'] and m not in rest: rest.append(m)
        return [chosen]+rest
    def health(self, timeout=1.5):
        out=[]
        for m in self.models:
            ok=False; error=''
            try:
                r=httpx.get(m['base_url'].rstrip('/')+'/models',timeout=timeout); ok=r.status_code<500
            except Exception as e: error=type(e).__name__
            out.append({**m,'online':ok,'error':error})
        return out

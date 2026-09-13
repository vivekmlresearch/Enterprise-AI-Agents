from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .api import router
from .config import ROOT, HOST, PORT

app=FastAPI(title='SovereignCodeAgent',version='0.3.0')
app.include_router(router,prefix='/api')
app.mount('/static',StaticFiles(directory=str(ROOT/'ui')),name='static')
@app.get('/')
def index(): return FileResponse(ROOT/'ui'/'index.html')

if __name__=='__main__':
    import uvicorn
    uvicorn.run('app.main:app',host=HOST,port=PORT,reload=False)

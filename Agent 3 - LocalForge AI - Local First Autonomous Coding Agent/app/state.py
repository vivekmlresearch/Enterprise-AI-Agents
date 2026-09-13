import json, sqlite3, time, uuid, threading
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks(
  id TEXT PRIMARY KEY, prompt TEXT, status TEXT, created REAL, updated REAL,
  model TEXT, iteration INTEGER DEFAULT 0, summary TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS events(
  id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT, ts REAL, kind TEXT, payload TEXT
);
CREATE TABLE IF NOT EXISTS checkpoints(
  id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT, ts REAL, iteration INTEGER, git_head TEXT, note TEXT
);
"""

class StateStore:
    def __init__(self, path: Path):
        self.path=path; path.parent.mkdir(parents=True,exist_ok=True)
        self.lock=threading.RLock()
        self.db=sqlite3.connect(path,check_same_thread=False)
        self.db.row_factory=sqlite3.Row
        with self.lock:
            self.db.executescript(SCHEMA); self.db.commit()
    def create_task(self,prompt,model=None,task_id=None):
        tid=task_id or uuid.uuid4().hex[:12]; now=time.time()
        with self.lock:
            self.db.execute("INSERT INTO tasks(id,prompt,status,created,updated,model) VALUES(?,?,?,?,?,?)",(tid,prompt,'running',now,now,model)); self.db.commit()
        return tid
    def event(self,task_id,kind,payload):
        with self.lock:
            self.db.execute("INSERT INTO events(task_id,ts,kind,payload) VALUES(?,?,?,?)",(task_id,time.time(),kind,json.dumps(payload,ensure_ascii=False)))
            self.db.execute("UPDATE tasks SET updated=? WHERE id=?",(time.time(),task_id)); self.db.commit()
    def checkpoint(self,task_id,iteration,git_head,note):
        with self.lock:
            self.db.execute("INSERT INTO checkpoints(task_id,ts,iteration,git_head,note) VALUES(?,?,?,?,?)",(task_id,time.time(),iteration,git_head,note)); self.db.commit()
    def finish(self,task_id,status,iteration,summary=''):
        with self.lock:
            self.db.execute("UPDATE tasks SET status=?,updated=?,iteration=?,summary=? WHERE id=?",(status,time.time(),iteration,summary,task_id)); self.db.commit()
    def tasks(self,limit=50):
        with self.lock: return [dict(r) for r in self.db.execute("SELECT * FROM tasks ORDER BY updated DESC LIMIT ?",(limit,)).fetchall()]
    def events_since(self,task_id,after=0,limit=200):
        with self.lock: rows=self.db.execute("SELECT * FROM events WHERE task_id=? AND id>? ORDER BY id LIMIT ?",(task_id,after,limit)).fetchall()
        return [{**dict(e),'payload':json.loads(e['payload'])} for e in rows]
    def task(self,task_id):
        with self.lock:
            row=self.db.execute("SELECT * FROM tasks WHERE id=?",(task_id,)).fetchone()
            if not row: return None
            ev=self.db.execute("SELECT * FROM events WHERE task_id=? ORDER BY id",(task_id,)).fetchall()
            cp=self.db.execute("SELECT * FROM checkpoints WHERE task_id=? ORDER BY id",(task_id,)).fetchall()
        out=dict(row); out['events']=[{**dict(e),'payload':json.loads(e['payload'])} for e in ev]; out['checkpoints']=[dict(c) for c in cp]; return out

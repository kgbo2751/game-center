from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os
import glob
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class LaunchRequest(BaseModel):
    category: str
    script: str

@app.get("/")
def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/games")
def get_games_list():
    project_root = os.path.dirname(os.path.dirname(__file__))
    base_dir = os.path.join(project_root, "games")
    
    games_2d = [os.path.basename(f) for f in glob.glob(os.path.join(base_dir, "2d_pygame", "*.py"))]
    games_3d = [os.path.basename(f) for f in glob.glob(os.path.join(base_dir, "3d_panda3d", "*.py"))]
    
    play_counts = {}
    try:
        res = requests.get("http://localhost:9000/api/stats")
        if res.status_code == 200:
            play_counts = res.json()
    except Exception:
        pass
    
    return {"games2d": games_2d, "games3d": games_3d, "playCounts": play_counts}

@app.post("/api/games/launch")
def launch_game(req: LaunchRequest):
    project_root = os.path.dirname(os.path.dirname(__file__))
    script_path = os.path.join(project_root, "games", req.category, req.script)
    
    subprocess.Popen(["python", script_path])
    
    try:
        java_api_url = f"http://localhost:9000/api/stats/increment"
        requests.post(java_api_url, params={"script": req.script})
    except Exception as e:
        print(e)
        
    return {"status": "SUCCESS"}

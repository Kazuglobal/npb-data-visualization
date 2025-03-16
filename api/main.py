from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Dict, List, Any
import os
from datetime import datetime

app = FastAPI(title="NPB Data API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_latest_data() -> Dict[str, Any]:
    """最新のデータファイルを読み込む"""
    data_dir = "../data"
    if not os.path.exists(data_dir):
        return {}
    
    files = [f for f in os.listdir(data_dir) if f.startswith("npb_players_")]
    if not files:
        return {}
    
    latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(data_dir, x)))
    with open(os.path.join(data_dir, latest_file), 'r', encoding='utf-8') as f:
        return json.load(f)

@app.get("/")
async def root():
    return {"message": "Welcome to NPB Data API"}

@app.get("/teams")
async def get_teams():
    data = get_latest_data()
    teams = []
    for team_id, players in data.items():
        if players:  # チームに選手が存在する場合
            team_info = {
                "id": team_id,
                "name": players[0]["team"],
                "league": players[0]["league"],
                "player_count": len(players)
            }
            teams.append(team_info)
    return teams

@app.get("/players/{team_id}")
async def get_team_players(team_id: str):
    data = get_latest_data()
    if team_id not in data:
        raise HTTPException(status_code=404, detail="Team not found")
    return data[team_id]

@app.get("/player/{player_id}")
async def get_player(player_id: str):
    data = get_latest_data()
    for team_players in data.values():
        for player in team_players:
            if player["id"] == player_id:
                return player
    raise HTTPException(status_code=404, detail="Player not found")

@app.get("/statistics")
async def get_statistics():
    data = get_latest_data()
    stats = {
        "total_players": sum(len(players) for players in data.values()),
        "teams": len(data),
        "last_updated": datetime.fromtimestamp(os.path.getctime("../data/" + 
            max(os.listdir("../data"), key=lambda x: os.path.getctime("../data/" + x))
        )).isoformat() if os.path.exists("../data") and os.listdir("../data") else None
    }
    return stats
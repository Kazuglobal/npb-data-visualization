from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any
import json
import os
from datetime import datetime

router = APIRouter()

def get_latest_teams_file() -> str:
    """Get the path to the latest teams JSON file"""
    data_dir = "../data"
    team_files = [f for f in os.listdir(data_dir) if f.startswith("npb_teams_")]
    if not team_files:
        raise HTTPException(status_code=404, detail="No team data found")
    return os.path.join(data_dir, sorted(team_files)[-1])

@router.get("/teams/{league}")
async def get_teams(league: str) -> List[Dict[str, Any]]:
    """Get teams by league (central/pacific)"""
    if league not in ["central", "pacific"]:
        raise HTTPException(status_code=400, detail="Invalid league. Must be 'central' or 'pacific'")
    
    try:
        with open(get_latest_teams_file(), 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data[league]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/teams")
async def get_all_teams() -> Dict[str, List[Dict[str, Any]]]:
    """Get all teams from both leagues"""
    try:
        with open(get_latest_teams_file(), 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/teams/last_updated")
async def get_last_updated() -> Dict[str, str]:
    """Get the timestamp of the last team data update"""
    try:
        latest_file = get_latest_teams_file()
        timestamp = os.path.basename(latest_file).split("_")[2].split(".")[0]
        dt = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
        return {"last_updated": dt.isoformat()}
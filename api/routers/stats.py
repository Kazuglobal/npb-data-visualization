from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any
import json
import os
from datetime import datetime

router = APIRouter()

def get_latest_stats_file() -> str:
    """Get the path to the latest stats JSON file"""
    data_dir = "../data"
    stats_files = [f for f in os.listdir(data_dir) if f.startswith("npb_stats_")]
    if not stats_files:
        raise HTTPException(status_code=404, detail="No statistics data found")
    return os.path.join(data_dir, sorted(stats_files)[-1])

@router.get("/team/{stats_type}")
async def get_team_stats(stats_type: str) -> List[Dict[str, Any]]:
    """Get team statistics for batting/pitching/fielding"""
    if stats_type not in ["batting", "pitching", "fielding"]:
        raise HTTPException(status_code=400, detail="Invalid stats type")
    
    try:
        with open(get_latest_stats_file(), 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data["team"][stats_type]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/individual/{stats_type}")
async def get_individual_stats(stats_type: str) -> List[Dict[str, Any]]:
    """Get individual player statistics for batting/pitching/fielding"""
    if stats_type not in ["batting", "pitching", "fielding"]:
        raise HTTPException(status_code=400, detail="Invalid stats type")
    
    try:
        with open(get_latest_stats_file(), 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data["individual"][stats_type]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/leaders/{stats_type}")
async def get_leaders(stats_type: str) -> List[Dict[str, Any]]:
    """Get statistical leaders for batting/pitching/fielding"""
    if stats_type not in ["batting", "pitching", "fielding"]:
        raise HTTPException(status_code=400, detail="Invalid stats type")
    
    try:
        with open(get_latest_stats_file(), 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data["leaders"][stats_type]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/last_updated")
async def get_last_updated() -> Dict[str, str]:
    """Get the timestamp of the last statistics update"""
    try:
        latest_file = get_latest_stats_file()
        timestamp = os.path.basename(latest_file).split("_")[2].split(".")[0]
        dt = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
        return {"last_updated": dt.isoformat()}
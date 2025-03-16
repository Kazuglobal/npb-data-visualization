import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import logging
from typing import Dict, List, Any
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NPBScraper:
    BASE_URL = "https://npb.jp"
    PLAYERS_URL = "https://npb.jp/bis/players/"
    
    TEAMS = {
        "giants": {"name": "読売ジャイアンツ", "league": "Central"},
        "tigers": {"name": "阪神タイガース", "league": "Central"},
        "baystars": {"name": "横浜DeNAベイスターズ", "league": "Central"},
        "carp": {"name": "広島東洋カープ", "league": "Central"},
        "swallows": {"name": "東京ヤクルトスワローズ", "league": "Central"},
        "dragons": {"name": "中日ドラゴンズ", "league": "Central"},
        "hawks": {"name": "福岡ソフトバンクホークス", "league": "Pacific"},
        "fighters": {"name": "北海道日本ハムファイターズ", "league": "Pacific"},
        "marines": {"name": "千葉ロッテマリーンズ", "league": "Pacific"},
        "eagles": {"name": "東北楽天ゴールデンイーグルス", "league": "Pacific"},
        "buffaloes": {"name": "オリックス・バファローズ", "league": "Pacific"},
        "lions": {"name": "埼玉西武ライオンズ", "league": "Pacific"}
    }

    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_player_list(self, team_id: str) -> List[Dict[str, Any]]:
        """Get list of players for a specific team"""
        try:
            team_url = f"{self.PLAYERS_URL}?team={team_id}"
            async with self.session.get(team_url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                players = []
                
                player_entries = soup.find_all('div', class_='player_entry')
                for entry in player_entries:
                    player_info = {
                        'id': entry.get('id', ''),
                        'name': entry.find('h4', class_='name').text.strip() if entry.find('h4', class_='name') else '',
                        'number': entry.find('div', class_='number').text.strip() if entry.find('div', class_='number') else '',
                        'position': entry.find('div', class_='position').text.strip() if entry.find('div', class_='position') else '',
                        'team': self.TEAMS[team_id]["name"],
                        'league': self.TEAMS[team_id]["league"],
                        'team_id': team_id,
                        'profile_url': self.BASE_URL + entry.find('a')['href'] if entry.find('a') else None
                    }
                    players.append(player_info)
                
                return players
        except Exception as e:
            logger.error(f"Error fetching player list for team {team_id}: {str(e)}")
            return []

    async def get_player_details(self, player_url: str) -> Dict[str, Any]:
        """Get detailed information for a specific player"""
        try:
            async with self.session.get(player_url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                details = {}
                profile_table = soup.find('table', class_='profile')
                if profile_table:
                    rows = profile_table.find_all('tr')
                    for row in rows:
                        header = row.find('th').text.strip() if row.find('th') else ''
                        value = row.find('td').text.strip() if row.find('td') else ''
                        details[header] = value

                # Extract statistics
                stats_tables = soup.find_all('table', class_='stats')
                if stats_tables:
                    stats = []
                    for table in stats_tables:
                        headers = [th.text.strip() for th in table.find_all('th')]
                        rows = table.find_all('tr')[1:]  # Skip header row
                        for row in rows:
                            values = [td.text.strip() for td in row.find_all('td')]
                            if len(headers) == len(values):
                                stats.append(dict(zip(headers, values)))
                    details['statistics'] = stats

                return details
        except Exception as e:
            logger.error(f"Error fetching player details from {player_url}: {str(e)}")
            return {}

    async def get_all_players(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all players from all teams with their details"""
        all_players = {}
        
        for team_id in self.TEAMS.keys():
            logger.info(f"Fetching players for team: {self.TEAMS[team_id]['name']}")
            players = await self.get_player_list(team_id)
            
            detailed_players = []
            for player in players:
                if player['profile_url']:
                    details = await self.get_player_details(player['profile_url'])
                    player.update(details)
                detailed_players.append(player)
            
            all_players[team_id] = detailed_players
            logger.info(f"Completed fetching {len(detailed_players)} players for {self.TEAMS[team_id]['name']}")
        
        return all_players

    def save_to_json(self, data: Dict[str, Any], filename: str = None):
        """Save scraped data to JSON file with timestamp"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/npb_players_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Data successfully saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving data to {filename}: {str(e)}")

async def main():
    async with NPBScraper() as scraper:
        all_players = await scraper.get_all_players()
        scraper.save_to_json(all_players)

if __name__ == "__main__":
    asyncio.run(main())
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import logging
from typing import Dict, List, Any
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NPBStatsScraper:
    BASE_URL = "https://npb.jp/bis/2024/stats/"
    
    STATS_TYPES = {
        "team": {
            "batting": "idb1t1.html",
            "pitching": "idp1t1.html",
            "fielding": "idf1t1.html"
        },
        "individual": {
            "batting": "idb1i1.html",
            "pitching": "idp1i1.html",
            "fielding": "idf1i1.html"
        },
        "leaders": {
            "batting": "idb1l1.html",
            "pitching": "idp1l1.html",
            "fielding": "idf1l1.html"
        }
    }

    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_team_stats(self, stats_type: str) -> List[Dict[str, Any]]:
        """Get team statistics (batting/pitching/fielding)"""
        try:
            url = f"{self.BASE_URL}{self.STATS_TYPES['team'][stats_type]}"
            async with self.session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                stats = []

                # Find the stats table
                table = soup.find('table', class_='tablesorter')
                if not table:
                    return []

                # Get headers
                headers = [th.text.strip() for th in table.find('thead').find_all('th')]

                # Get team stats
                for row in table.find('tbody').find_all('tr'):
                    values = [td.text.strip() for td in row.find_all('td')]
                    if len(headers) == len(values):
                        stats.append(dict(zip(headers, values)))

                return stats
        except Exception as e:
            logger.error(f"Error fetching {stats_type} team stats: {str(e)}")
            return []

    async def get_individual_stats(self, stats_type: str) -> List[Dict[str, Any]]:
        """Get individual player statistics (batting/pitching/fielding)"""
        try:
            url = f"{self.BASE_URL}{self.STATS_TYPES['individual'][stats_type]}"
            async with self.session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                stats = []

                # Find the stats table
                table = soup.find('table', class_='tablesorter')
                if not table:
                    return []

                # Get headers
                headers = [th.text.strip() for th in table.find('thead').find_all('th')]

                # Get player stats
                for row in table.find('tbody').find_all('tr'):
                    values = [td.text.strip() for td in row.find_all('td')]
                    if len(headers) == len(values):
                        stats.append(dict(zip(headers, values)))

                return stats
        except Exception as e:
            logger.error(f"Error fetching {stats_type} individual stats: {str(e)}")
            return []

    async def get_leaders(self, stats_type: str) -> List[Dict[str, Any]]:
        """Get statistical leaders (batting/pitching/fielding)"""
        try:
            url = f"{self.BASE_URL}{self.STATS_TYPES['leaders'][stats_type]}"
            async with self.session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                leaders = []

                # Find all leader sections
                sections = soup.find_all('div', class_='leader_section')
                for section in sections:
                    category = section.find('h3').text.strip()
                    table = section.find('table')
                    if table:
                        headers = [th.text.strip() for th in table.find_all('th')]
                        rows = []
                        for tr in table.find_all('tr')[1:]:  # Skip header row
                            values = [td.text.strip() for td in tr.find_all('td')]
                            if len(headers) == len(values):
                                rows.append(dict(zip(headers, values)))
                        leaders.append({
                            "category": category,
                            "rankings": rows
                        })

                return leaders
        except Exception as e:
            logger.error(f"Error fetching {stats_type} leaders: {str(e)}")
            return []

    async def get_all_stats(self) -> Dict[str, Any]:
        """Get all available statistics"""
        stats = {
            "team": {},
            "individual": {},
            "leaders": {}
        }

        # Collect team stats
        for stats_type in self.STATS_TYPES["team"]:
            logger.info(f"Fetching team {stats_type} statistics...")
            stats["team"][stats_type] = await self.get_team_stats(stats_type)

        # Collect individual stats
        for stats_type in self.STATS_TYPES["individual"]:
            logger.info(f"Fetching individual {stats_type} statistics...")
            stats["individual"][stats_type] = await self.get_individual_stats(stats_type)

        # Collect leaders
        for stats_type in self.STATS_TYPES["leaders"]:
            logger.info(f"Fetching {stats_type} leaders...")
            stats["leaders"][stats_type] = await self.get_leaders(stats_type)

        return stats

    def save_to_json(self, data: Dict[str, Any], filename: str = None):
        """Save scraped statistics to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/npb_stats_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Statistics successfully saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving statistics to {filename}: {str(e)}")

async def main():
    async with NPBStatsScraper() as scraper:
        stats = await scraper.get_all_stats()
        scraper.save_to_json(stats)

if __name__ == "__main__":
    asyncio.run(main())
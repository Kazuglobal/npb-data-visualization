from playwright.sync_api import sync_playwright
import json
import logging
from typing import Dict, List, Any
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NPBTeamScraper:
    BASE_URL = "https://npb.jp/teams/"
    
    def __init__(self):
        self.teams_data = {
            "central": [],
            "pacific": []
        }

    def scrape_teams(self):
        """Scrape NPB team information using Playwright"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                logger.info("Accessing NPB teams page...")
                page.goto(self.BASE_URL)
                page.wait_for_load_state("networkidle")

                # セ・リーグチーム情報の取得
                logger.info("Scraping Central League teams...")
                central_teams = page.query_selector_all('//h3[contains(text(), "CENTRAL LEAGUE")]/following-sibling::div[1]//table')
                self.teams_data["central"] = self._extract_teams_data(central_teams)

                # パ・リーグチーム情報の取得
                logger.info("Scraping Pacific League teams...")
                pacific_teams = page.query_selector_all('//h3[contains(text(), "PACIFIC LEAGUE")]/following-sibling::div[1]//table')
                self.teams_data["pacific"] = self._extract_teams_data(pacific_teams)

            except Exception as e:
                logger.error(f"Error during scraping: {str(e)}")
            finally:
                browser.close()

        return self.teams_data

    def _extract_teams_data(self, team_elements) -> List[Dict[str, Any]]:
        """Extract team information from table elements"""
        teams = []
        
        for team_element in team_elements:
            try:
                # チーム名の取得（日本語と英語）
                team_name = team_element.evaluate('(el) => {
                    const prevElement = el.previousElementSibling;
                    if (prevElement && prevElement.tagName === "H4") {
                        return {
                            ja: prevElement.textContent.split(/(?=[A-Z])/)[0].trim(),
                            en: prevElement.textContent.split(/(?=[A-Z])/)[1].trim()
                        };
                    }
                    return null;
                }')

                if not team_name:
                    continue

                # チーム詳細情報の取得
                rows = team_element.query_selector_all('tr')
                team_info = {
                    "name": team_name,
                    "details": {}
                }

                for row in rows:
                    cells = row.query_selector_all('td')
                    if len(cells) == 2:
                        key = cells[0].inner_text().strip()
                        value = cells[1].inner_text().strip()
                        
                        # 本拠地の場合、球場名のみを抽出
                        if "本拠地" in key:
                            value = value.split("/")[0].strip()
                        
                        team_info["details"][key] = value

                # チームロゴURLの取得（存在する場合）
                logo_element = team_element.evaluate('(el) => {
                    const img = el.closest("div").querySelector("img");
                    return img ? img.src : null;
                }')
                
                if logo_element:
                    team_info["logo_url"] = logo_element

                teams.append(team_info)

            except Exception as e:
                logger.error(f"Error extracting team data: {str(e)}")
                continue

        return teams

    def save_to_json(self, filename: str = None):
        """Save scraped team data to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/npb_teams_{timestamp}.json"

        # データディレクトリの作成（存在しない場合）
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.teams_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Team data successfully saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving team data to {filename}: {str(e)}")

def main():
    scraper = NPBTeamScraper()
    scraper.scrape_teams()
    scraper.save_to_json()

if __name__ == "__main__":
    main()
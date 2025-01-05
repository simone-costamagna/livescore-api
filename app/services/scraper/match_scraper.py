import logging
import re
from app.services.models.match_schemas import Match
from app.services.scraper.scraper import Scraper
import os
from dotenv import load_dotenv
from app.services.utils import get_match_datetime

load_dotenv()

URL_LIVESPORT_MATCH = os.getenv('URL_LIVESPORT_MATCH')
XPATH_ROUND = '//*[@id="detail"]/div[3]/div/span[3]/a'
XPATH_DATETIME = '//*[@id="detail"]/div[4]/div[1]/div'
XPATH_HOME_TEAM = '//*[@id="detail"]/div[4]/div[2]/div[3]/div[2]/a'
XPATH_AWAY_TEAM = '//*[@id="detail"]/div[4]/div[4]/div[3]/div[1]/a'
XPATH_STATS_BUTTON = '//*[@id="detail"]/div[7]/div/a[2]'
XPATH_HOME_SCORE = '//*[@id="detail"]/div[4]/div[3]/div[1]/div[1]/span[1]'
XPATH_AWAY_SCORE = '//*[@id="detail"]/div[4]/div[3]/div[1]/div[1]/span[3]'
XPATH_STATS = '//*[@id="detail"]/div[9]/div'
XPATH_NAME_STAT = './div[1]/div[2]/strong[1]'
XPATH_FIRST_STAT = './div[1]/div[1]/strong[1]'
XPATH_SECOND_STAT = './div[1]/div[3]/strong[1]'
stat_mapping = {
    'Expected Goals (xG)': lambda f, s: (float(f), float(s)),
    'Ball Possession': lambda f, s: (int(f.replace('%', '')), int(s.replace('%', ''))),
    'Goal Attempts': lambda f, s: (int(f), int(s)),
    'Shots on Goal': lambda f, s: (int(f), int(s)),
    'Shots off Goal': lambda f, s: (int(f), int(s)),
    'Big Chances': lambda f, s: (int(f), int(s)),
    'Corner Kicks': lambda f, s: (int(f), int(s)),
    'Free Kicks': lambda f, s: (int(f), int(s)),
    'Offsides': lambda f, s: (int(f), int(s)),
    'Fouls': lambda f, s: (int(f), int(s)),
    'Yellow Cards': lambda f, s: (int(f), int(s)),
    'Red Cards': lambda f, s: (int(f), int(s)),
}


class MatchScraper(Scraper):
    """
    Handles the scraping of match data.

    Inherits from:
        Scraper: Provides base functionality for web scraping using Selenium.
    """
    def __init__(self) -> None:
        super().__init__()

    def scrape_match(self, match_id: str) -> Match:
        """
        Scrapes match data for a specific match identified by its ID.

        Args:
            match_id (str): The unique identifier of the match.

        Returns:
            Match: The scraped match data.
        """
        logging.debug(f"Processing match: {match_id}")

        self.get_page(URL_LIVESPORT_MATCH.replace('{MATCH_ID}', match_id))
        logging.debug(f"Reached URL {URL_LIVESPORT_MATCH.replace('{MATCH_ID}', match_id)}")

        match = Match(id=match_id)
        round_element = self.find_element(XPATH_ROUND)
        match.round = int(re.search(r'ROUND (\d+)', (round_element.text)).group(1))
        datetime_element = self.find_element(XPATH_DATETIME)
        match.match_date = get_match_datetime(datetime_element.text)
        home_element = self.find_element(XPATH_HOME_TEAM)
        match.home = home_element.text
        away_element = self.find_element(XPATH_AWAY_TEAM)
        match.away = away_element.text

        read_stats = True
        try:
            self.find_element(XPATH_STATS_BUTTON, temporary=True)
            logging.debug("The match is played, stats are available")
        except Exception as ex:
            logging.debug("The match hasn't already played, stats are not available")
            read_stats = False

        if read_stats:
            home_score_element = self.find_element(XPATH_HOME_SCORE)
            match.home_score = int(home_score_element.text)
            away_score_element = self.find_element(XPATH_AWAY_SCORE)
            match.away_score = int(away_score_element.text)

            stats_elements = self.find_elements(XPATH_STATS)
            for stat_element in stats_elements:
                name_stat_element = self.find_element(XPATH_NAME_STAT, stat_element)
                name_element = name_stat_element.text
                first_stat_element = self.find_element(XPATH_FIRST_STAT, stat_element)
                first_stat = first_stat_element.text
                second_stat_element = self.find_element(XPATH_SECOND_STAT, stat_element)
                second_stat = second_stat_element.text

                if name_element in stat_mapping:
                    setattr(match, name_element.lower().replace(' ', '_').replace('(', '').replace(')', ''),
                            stat_mapping[name_element](first_stat, second_stat))

        return match

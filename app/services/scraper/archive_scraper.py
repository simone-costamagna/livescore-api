import logging
import re

from anyio import sleep

from app.services.models.archive_schemas import Archive, Match, Rank, LiveMatch
from app.services.models.utils import Pagination
from app.services.scraper.leagues_scraper import LeagueScraper
from app.services.scraper.scraper import Scraper
from app.services.utils import get_match_datetime
import os
from dotenv import load_dotenv

load_dotenv()

LIMIT = int(os.getenv("LIMIT"))
XPATH_TABS_MENU = "//div[@class='container__heading']/div[3]/div[1]/a"
XPATH_NO_FOUND_MATCH = "//*[@id='no-match-found']"
XPATH_SHOW_MORE_RESULTS = "//*[@id='live-table']/div[1]/div/div/a"
XPATH_ROUNDS_RESULTS = "//div[contains(@class, 'event__round')]"
XPATH_MATCH_RESULTS = "//*[@id='live-table']/div[1]/div/div/div[contains(@class, 'event__match')]"
XPATH_MATCH_RESULTS_FROM_ROUND = "./following-sibling::div[contains(@class, 'event__match')]"
XPATH_DATE_MATCH = "./div[1]"
XPATH_ID_MATCH = "./a[1]"
XPATH_HOME_MATCH = ".//div[contains(@class, 'homeParticipant')]//span | .//div[contains(@class, 'homeParticipant')]//strong"
XPATH_AWAY_MATCH = ".//div[contains(@class, 'awayParticipant')]//span | .//div[contains(@class, 'awayParticipant')]//strong"
XPATH_HOME_SCORE_MATCH = "./div[4]"
XPATH_AWAY_SCORE_MATCH = "./div[5]"
XPATH_TABLE_STANDING = "//div[@class='ui-table__body']/div"
XPATH_TEAM_ELEMENT_FROM_STANDING = "./div[2]/div[1]/div[1]/a[2]"
XPATH_MP_ELEMENT_FROM_STANDING = "./span[1]"
XPATH_W_ELEMENT_FROM_STANDING = "./span[2]"
XPATH_D_ELEMENT_FROM_STANDING = "./span[3]"
XPATH_L_ELEMENT_FROM_STANDING = "./span[4]"
XPATH_GOALS_ELEMENT_FROM_STANDING = "./span[5]"
XPATH_PTS_ELEMENT_FROM_STANDING = "./span[7]"
XPATH_LIVE_MATCHES = '//*[@id="live-table"]/section[1]/div/div[2]/div[contains(@class, "live")]'
XPATH_ID_FROM_LIVE_MATCH = './a[1]'
XPATH_TIME_FROM_LIVE_MATCH = './div[1]/div[1]'
XPATH_HOME_FROM_LIVE_MATCH = './div[2]/span[1]'
XPATH_AWAY_FROM_LIVE_MATCH = './div[3]/span[1]'
XPATH_HOME_SCORE_FROM_LIVE_MATCH = './div[4]'
XPATH_AWAY_SCORE_FROM_LIVE_MATCH = './div[5]'

MENU_MAPPING = {
    'SUMMARY': 'live',
    'RESULTS': 'results',
    'FIXTURES': 'fixtures',
    'STANDINGS': 'standings'
}
CONFIG_SCORE = 'score'

class ArchiveScraper(Scraper):
    """
    Handles the scraping of archive data and match results.

    Inherits from:
        Scraper: Provides base functionality for web scraping using Selenium.
    """
    def __init__(self) -> None:
        super().__init__()

    def scrape_archive(self, archive_id: str) -> Archive:
        """
        Scrapes archive data for a given archive ID.

        Args:
            archive_id (str): The unique identifier for the archive.

        Returns:
            Archive: The scraped archive data, or None if not found.
        """
        logging.debug(f"Processing archive ID: {archive_id}")

        match = re.match(r"^(.*?)-(.*?)-(\d{4}_\d{4})$", archive_id)
        if match:
            country, league, season = match.groups()
            logging.debug(f"Extracted details - Country: {country}, League: {league}, Season: {season}")

            league_scraper = LeagueScraper()
            league_id = f"{country}-{league}"
            archives = league_scraper.scrape_league_archives(league_id)

            url = next((archive.url for archive in archives if archive.season == season), None)

            if url is None:
                logging.warning(f"Archive '{season}' not found in league '{league}'")
                return None

            self.get_page(url)

            archive = Archive()
            archive.league = league_id
            archive.season = season
            archive.url = url

            menu_elements = self.find_elements(XPATH_TABS_MENU)
            for menu_element in menu_elements:
                menu_text = menu_element.text.strip()
                if menu_text in MENU_MAPPING:
                    setattr(archive, MENU_MAPPING[menu_text], self.get_attribute(menu_element))

            return archive if archive.validate() else None
        else:
            logging.debug(f"Invalid Archive ID: {archive_id}")
            return None


    def scrape_results_by_archive(self, archive_id: str, page: int, size: int) -> tuple[list[Match], Pagination]:
        """
        Scrapes match results for a given archive, with pagination support.

        Args:
            archive_id (str): The unique identifier for the archive.
            page (int): The page number to retrieve.
            size (int): The number of items per page.

        Returns:
            tuple[list[Match], Pagination]: A list of matches and the pagination details.
        """
        archive = self.scrape_archive(archive_id)

        if archive is None:
            logging.debug(f"The archive {archive_id} does not exist.")
            raise ValueError(f"The archive {archive_id} does not exist")

        config = {
            CONFIG_SCORE: True
        }
        matches, pagination = self.scrape_matches(archive.results, archive, page, size, config)

        return matches, pagination


    def scrape_fixtures_by_archive(self, archive_id: str, page: int, size: int) -> tuple[list[Match], Pagination]:
        """
        Scrapes fixtures for a given archive, with pagination support.

        Args:
            archive_id (str): The unique identifier for the archive.
            page (int): The page number to retrieve.
            size (int): The number of items per page.

        Returns:
            tuple[list[Match], Pagination]: A list of fixtures and the pagination details.
        """
        archive = self.scrape_archive(archive_id)

        if archive is None:
            logging.debug(f"The archive {archive_id} does not exist.")
            raise ValueError(f"The archive {archive_id} does not exist")

        config = {
            CONFIG_SCORE: False
        }
        matches, pagination = self.scrape_matches(archive.fixtures, archive, page, size, config)

        return matches, pagination


    def scrape_live_by_archive(self, archive_id: str) -> list[LiveMatch]:
        """
        Scrapes live match data for a given archive.

        Args:
            archive_id (str): The unique identifier for the archive.

        Returns:
            list[LiveMatch]: A list of live matches.
        """
        archive = self.scrape_archive(archive_id)

        if archive is None:
            logging.debug(f"The archive {archive_id} does not exist.")
            raise ValueError(f"The archive {archive_id} does not exist")

        self.get_page(archive.live)
        logging.debug(f"Reached URL: {archive.live}")

        live_match_elements = self.find_elements(XPATH_LIVE_MATCHES)
        matches = []

        for live_match_element in live_match_elements:
            match = LiveMatch()
            match.archive = archive.id
            id_element = self.find_element(XPATH_ID_FROM_LIVE_MATCH, live_match_element)
            match.url = id_element.get_attribute("href")
            match.id = re.search(r'/match/([^/]+)/', match.url).group(1)
            time_element = self.find_element(XPATH_TIME_FROM_LIVE_MATCH, live_match_element)
            match.time = time_element.text
            home_element = self.find_element(XPATH_HOME_FROM_LIVE_MATCH, live_match_element)
            match.home = home_element.text
            away_element = self.find_element(XPATH_AWAY_FROM_LIVE_MATCH, live_match_element)
            match.away = away_element.text
            home_score_element = self.find_element(XPATH_HOME_SCORE_FROM_LIVE_MATCH, live_match_element)
            match.home_score = int(home_score_element.text)
            away_score_element = self.find_element(XPATH_AWAY_SCORE_FROM_LIVE_MATCH, live_match_element)
            match.away_score = int(away_score_element.text)

            matches.append(match)

        return matches


    def scrape_matches(self, url: str, archive: Archive, page: int, size: int, config: dict) -> tuple[list[Match], Pagination]:
        """
        Scrapes match data from a given URL with pagination.

        Args:
            url (str): The URL to scrape match data from.
            archive (Archive): The archive metadata associated with the matches.
            page (int): The page number to retrieve.
            size (int): The number of items per page.
            config (dict): Configuration options for scraping.

        Returns:
            tuple[list[Match], Pagination]: A list of matches and the pagination details.
        """
        self.get_page(url)
        logging.debug(f"Scraping matches: reached URL {url}")

        try:
            self.find_element(XPATH_NO_FOUND_MATCH, temporary=True)
            logging.debug(f"No match found for URL {url}")
            return [[], None]
        except Exception as e:
            logging.debug(f"Some match exist for URL {url}")

        end = True
        counter = 0
        while end and counter < LIMIT:
            try:
                show_more_button = self.find_element(XPATH_SHOW_MORE_RESULTS, temporary=True)
                self.execute_script(show_more_button)
                counter += 1
            except Exception as ex:
                end = False
                logging.debug("Finished expanding results.")

        match_elements = self.find_elements(XPATH_MATCH_RESULTS)
        logging.debug(f"Found {len(match_elements)} matches")

        try:
            total_items = len(match_elements)
            if page == 0:  # Return all items if page is 0
                start, end = 0, total_items
                current_page, total_pages = 0, 1
            else:
                start = (page - 1) * size
                end = start + size
                if start >= total_items:
                    raise ValueError("Invalid pagination: page exceeds total items.")
                current_page = page
                total_pages = (total_items + size - 1) // size

            # Build the pagination object
            pagination = Pagination(
                current_page=current_page,
                page_size=size if page != 0 else total_items,
                total_items=total_items,
                total_pages=total_pages
            )
        except ValueError as ex:
            logging.error(f"Pagination error: {ex}")
            raise
        except Exception as ex:
            logging.error("Unexpected error during pagination")
            raise ValueError("Invalid pagination")

        round_elements = self.find_elements(XPATH_ROUNDS_RESULTS)
        counter = 0
        matches = []
        for round_element in round_elements:
            if counter > end:
                break
            round = int(re.search(r'\d+', round_element.text.strip()).group())

            # Find the sibling event_match divs under the current round
            match_elements = self.find_elements(XPATH_MATCH_RESULTS_FROM_ROUND, element=round_element)

            # Stop collecting matches when the next round div appears
            for match_element in match_elements:
                if 'event__round' in match_element.get_attribute('class'):
                    break

                if counter >= start and counter < end:
                    # Extract match data
                    match = Match()
                    match.archive = archive.id
                    match.round = round
                    try:
                        id_element = self.find_element(XPATH_ID_MATCH, element=match_element)
                        match.url = self.get_attribute(id_element)
                        match.id = re.search(r'/match/([^/]+)/', match.url).group(1)
                        date_element = self.find_element(XPATH_DATE_MATCH, element=match_element)
                        match.match_date = get_match_datetime(date_element.text.strip(), archive.season)
                        home_element = self.find_element(XPATH_HOME_MATCH, element=match_element)
                        match.home = home_element.text.strip()
                        away_element = self.find_element(XPATH_AWAY_MATCH, element=match_element)
                        match.away = away_element.text.strip()
                        if config[CONFIG_SCORE]:
                            home_score_element = self.find_element(XPATH_HOME_SCORE_MATCH, element=match_element)
                            match.home_score = int(home_score_element.text.strip())
                            away_score_element = self.find_element(XPATH_AWAY_SCORE_MATCH, element=match_element)
                            match.away_score = int(away_score_element.text.strip())
                    except Exception as ex:
                        logging.warning(f"Unable to extract full information for match at index {counter}: {ex}")

                    matches.append(match)

                counter += 1

        return matches, pagination


    def scrape_standings_by_archive(self, archive_id: str) -> list[Rank]:
        """
        Scrapes standings data for a given archive.

        Args:
            archive_id (str): The unique identifier for the archive.

        Returns:
            list[Rank]: A list of rankings with team and performance details.
        """
        archive = self.scrape_archive(archive_id)

        if archive is None:
            logging.debug(f"The archive {archive_id} does not exist.")
            raise ValueError(f"The archive {archive_id} does not exist")

        self.get_page(archive.standings)

        ranking_elements = self.find_elements(XPATH_TABLE_STANDING)
        standings = []
        for index, ranking_element in enumerate(ranking_elements):
            rank = Rank(position=index+1)
            team_element = self.find_element(XPATH_TEAM_ELEMENT_FROM_STANDING, ranking_element)
            rank.team = team_element.text.strip()
            mp_element = self.find_element(XPATH_MP_ELEMENT_FROM_STANDING, ranking_element)
            rank.matches_played = int(mp_element.text.strip())
            w_element = self.find_element(XPATH_W_ELEMENT_FROM_STANDING, ranking_element)
            rank.wins = int(w_element.text.strip())
            d_element = self.find_element(XPATH_D_ELEMENT_FROM_STANDING, ranking_element)
            rank.draws = int(d_element.text.strip())
            l_element = self.find_element(XPATH_L_ELEMENT_FROM_STANDING, ranking_element)
            rank.losses = int(l_element.text.strip())
            goals_element = self.find_element(XPATH_GOALS_ELEMENT_FROM_STANDING, ranking_element)
            rank.goals_scored = int(goals_element.text.strip().split(":")[0])
            rank.goals_conceded = int(goals_element.text.strip().split(":")[1])
            pts_element = self.find_element(XPATH_PTS_ELEMENT_FROM_STANDING, ranking_element)
            rank.points = int(pts_element.text.strip())
            standings.append(rank)

        return standings

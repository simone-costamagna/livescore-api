import logging
import re
from app.services.models.league_schemas import League, Archive
from app.services.scraper.country_scraper import CountryScraper
from app.services.scraper.scraper import Scraper

XPATH_ARCHIVE_ELEMENT = '//a[@class="tabs__tab archive"]'
XPATH_LEAGUE_ARCHIVE_LIST = '//*[@id="tournament-page-archiv"]/div[contains(@class, "archive__row")]'
XPATH_ARCHIVE_SEASON = './div[1]/a'
XPATH_ARCHIVE_WINNER = './div[2]/div[1]/a'

class LeagueScraper(Scraper):
    """
    A scraper class to extract league details and archives from the LiveScore website.

    Inherits from:
        Scraper: Provides base functionality for web scraping using Selenium.
    """
    def __init__(self) -> None:
        super().__init__()

    def scrape_league(self, league_id: str) -> League:
        """
        Scrapes details of a specific league identified by its league ID.

        Args:
            league_id (str): The unique identifier of the league.

        Returns:
            League: The scraped league object, or None if not found or invalid.
        """
        logging.debug(f"Processing league ID: {league_id}")

        try:
            country, league_name = league_id.split("-", 1)
        except ValueError:
            logging.warning(f"Invalid league ID: {league_id}")
            return None

        logging.debug(f"Scraping leagues for country: {country}")

        country_scraper = CountryScraper()
        leagues = country_scraper.scrape_leagues_by_country(country)

        url = next((league.url for league in leagues if league.name == league_name), None)

        if url is None:
            logging.warning(f"League '{league_name}' not found in country '{country}'")
            return None

        logging.debug(f"Reaching league URL: {url}")
        self.get_page(url)

        league = League(country=country, name=league_name, url=url)

        return league

    def scrape_league_archives(self, league_id: str) -> list[Archive]:
        """
        Scrapes archives for a specific league identified by its league ID.

        Args:
            league_id (str): The unique identifier of the league.

        Returns:
            list[Archive]: A list of Archive objects containing archive details for the specified league.
        """
        league = self.scrape_league(league_id)

        if league is None:
            logging.debug(f"The league {league_id} doesn't exist")
            raise ValueError(f"The league {league_id} doesn't exist")

        self.get_page(league.url)
        logging.debug(f"Reached league URL {league.url}")

        archive_element = self.find_element(XPATH_ARCHIVE_ELEMENT)
        archive_url = self.get_attribute(archive_element)
        self.get_page(archive_url)
        logging.debug(f"Reached archive league URL {archive_url}")

        archive_elements = self.find_elements(XPATH_LEAGUE_ARCHIVE_LIST)
        archives = []
        for archive_element in archive_elements:
            archive_season_element = self.find_element(XPATH_ARCHIVE_SEASON, element=archive_element)
            archive_season = re.search(r"\b(\d{4}/\d{4})\b", archive_season_element.text.strip()).group(1).replace("/", "_")
            try:
                archive_winner = self.find_element(XPATH_ARCHIVE_WINNER, element=archive_element)
                archive = Archive(league=league_id, season=archive_season, url=self.get_attribute(archive_season_element), winner=archive_winner)
            except Exception as ex:
                archive = Archive(league=league_id, season=archive_season, url=self.get_attribute(archive_season_element))
                logging.debug(f"Archive {archive_season} of league {league_id} doesn't have a winner")

            archives.append(archive)

        return archives

import logging
from app.services.models.country_schemas import Country, League
from app.services.scraper.scraper import Scraper
from app.services.utils import calculate_similarity

XPATH_SHOW_MORE_COUNTRIES = "//span[@class='lmc__itemMore']"
XPATH_COUNTRIES = "//div[@class='lmc__block ']"
XPATH_COUNTRY_NAME = "./a/span[1]"
XPATH_COUNTRY_URL = "./a"
XPATH_SHOW_MORE_LEAGUES = "//div[@class='show-more leftMenu__item leftMenu__item--more']"
XPATH_LEAGUES = "//div[@class='leftMenu__item leftMenu__item--width '] | //div[@class='leftMenu__item leftMenu__item--width']"
XPATH_LEAGUE_NAME = "./a"

class CountryScraper(Scraper):
    """
    A scraper class to extract country details from the LiveScore website.

    Inherits from:
        Scraper: Provides base functionality for web scraping using Selenium.
    """
    def __init__(self) -> None:
        super().__init__()

    def scrape_countries(self, country_search: str = None, exact_match: bool = False) -> list[Country]:
        """
        Scrapes all available countries from the LiveScore website.

        Args:
            country_search (str, optional): The specific country to search for. Defaults to None.
            exact_match (bool, optional): If True, use strict equality for matching instead of similarity. Defaults to False.

        Returns:
            list[Country]: A list of Country objects containing the name and URL of each country.
        """
        logging.debug("Scraping countries...")
        show_more_button = self.find_element(XPATH_SHOW_MORE_COUNTRIES)
        self.execute_script(show_more_button)

        countries_element = self.find_elements(XPATH_COUNTRIES)
        countries = []
        for country_element in countries_element:
            country_name_element = self.find_element(XPATH_COUNTRY_NAME, element=country_element)
            if country_name_element.text.strip():
                country_name = country_name_element.text.strip()

                if (country_search is None or (exact_match and country_search == country_name) or
                        (not exact_match and calculate_similarity(country_search, country_name))):
                    country_url_element = self.find_element(XPATH_COUNTRY_URL, element=country_element)
                    country_url = self.get_attribute(country_url_element)

                    country = Country(name=country_name, url=country_url)
                    countries.append(country)
                    if exact_match:
                        break

        logging.debug("Countries scraped")
        return countries

    def scrape_leagues_by_country(self, country_id: str) -> list[League]:
        """
        Scrapes all available leagues for a specific country from the LiveScore website.

        Args:
            country_id (str): The unique identifier of the country to search for leagues.

        Returns:
            list[League]: A list of League objects containing league details for the specified country.
        """
        logging.debug("Scraping leagues by country...")

        response = self.scrape_countries(country_search=country_id, exact_match=True)
        if response is None or len(response) != 1:
            return []

        country = response[0]
        self.get_page(country.url)

        logging.debug("Show more elements...")
        show_more_button = self.find_element(XPATH_SHOW_MORE_LEAGUES)
        self.execute_script(show_more_button)

        logging.debug("Finding leagues element...")
        leagues_element = self.find_elements(XPATH_LEAGUES)
        leagues = []
        for league_element in leagues_element:
            league_name_element = self.find_element(XPATH_LEAGUE_NAME, element=league_element)
            if league_name_element.text.strip():
                league_name = league_name_element.text.strip()
                league_url = self.get_attribute(league_name_element)
                league = League(country=country.name, url=league_url, name=league_name)
                leagues.append(league)

        logging.debug("Country's leagues scraped")
        return leagues
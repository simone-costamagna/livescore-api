import logging
from fastapi import APIRouter, HTTPException
from app.services.models.league_schemas import LeagueResponse, ArchiveListResponse
from app.services.scraper.leagues_scraper import LeagueScraper

ROUTER_NAME = 'leagues'

router = APIRouter()

@router.get("/{leagueId}", response_model=LeagueResponse)
def get_league(leagueId: str) -> LeagueResponse:
    """
    Retrieves detailed information about a specific league.

    Args:
        leagueId (str): The unique identifier of the league to scrape.

    Returns:
        LeagueResponse: The scraped league information.
    """
    try:
        logging.info(f"GET /{ROUTER_NAME}/{leagueId} - Starting league scraping process.")
        league_scraper = LeagueScraper()
        league = league_scraper.scrape_league(leagueId)

        if league is None:
            logging.warning(f"League with ID {leagueId} not found.")
            raise HTTPException(status_code=404, detail=f"League with ID {leagueId} not found.")

        logging.info(f"GET /{ROUTER_NAME}/{leagueId} call successful - League {leagueId} found.")
        return LeagueResponse(league=league)
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error occurred while processing league {leagueId}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{leagueId}/archives", response_model=ArchiveListResponse)
def get_archives_by_league(leagueId: str) -> ArchiveListResponse:
    """
    Retrieves all archives associated with a specific league.

    Args:
        leagueId (str): The unique identifier of the league to scrape archives from.

    Returns:
        ArchiveListResponse: A list of archives for the specified league.
    """
    try:
        logging.info(f"GET /{ROUTER_NAME}/{leagueId}/archives - Starting league's archive scraping process.")
        league_scraper = LeagueScraper()
        archives = league_scraper.scrape_league_archives(leagueId)

        logging.info(f"GET /{ROUTER_NAME}/{leagueId}/archives call successful - Found {len(archives)} archives.")
        return ArchiveListResponse(archives=archives)
    except Exception as e:
        logging.error(f"Error occurred while processing archives for league {leagueId}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
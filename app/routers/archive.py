import logging
from fastapi import APIRouter, HTTPException
from fastapi import Query
from app.services.models.archive_schemas import ArchiveResponse, MatchListResponse, StandingResponse, \
    ListLiveMatch
from app.services.scraper.archive_scraper import ArchiveScraper

ROUTER_NAME = 'archives'

router = APIRouter()

@router.get("/{archiveId}", response_model=ArchiveResponse)
def get_archive(archiveId: str) -> ArchiveResponse:
    """
    Retrieves the archive data by its ID.

    Args:
        archiveId (str): The unique identifier of the archive to scrape.

    Returns:
        ArchiveResponse: The scraped archive data.
    """
    try:
        logging.info(f"GET /{ROUTER_NAME}/{archiveId} - Starting archive scraping process.")
        archive_scraper = ArchiveScraper()
        archive = archive_scraper.scrape_archive(archiveId)

        if archive is None:
            logging.warning(f"Archive with ID {archiveId} not found.")
            raise HTTPException(status_code=404, detail=f"Archive with ID {archiveId} not found.")

        logging.info(f"GET /{ROUTER_NAME}/{archiveId} call successful - Archive {archiveId} scraped.")
        return ArchiveResponse(archive=archive)
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error occurred while processing archive {archiveId}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{archiveId}/results", response_model=MatchListResponse)
def get_results_by_archive(
    archiveId: str,
    page: int = Query(1, ge=0, description="Page number to retrieve, starting from 1. Use 0 to get all results."),
    size: int = Query(10, ge=0, le=100, description="Number of items per page (max 100). Use 0 to get all results.")
) -> MatchListResponse:
    """
    Retrieves paginated match results for a given archive.

    Args:
        archiveId (str): The unique identifier of the archive to scrape matches from.
        page (int, optional): The page number to retrieve. Defaults to 1.
        size (int, optional): The number of items per page (maximum 100). Defaults to 10.

    Returns:
        MatchListResponse: A paginated list of match results.
    """
    try:
        logging.info(f"GET /{ROUTER_NAME}/{archiveId}/results - Starting archive results scraping process.")
        archive_scraper = ArchiveScraper()
        matches, pagination = archive_scraper.scrape_results_by_archive(archiveId, page, size)

        logging.info(f"GET /{ROUTER_NAME}/{archiveId}/results call successful - Results of archive {archiveId} scraped.")
        return MatchListResponse(matches=matches, pagination=pagination)
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error occurred while processing results for archive {archiveId}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{archiveId}/fixtures", response_model=MatchListResponse)
def get_fixtures_by_archive(
    archiveId: str,
    page: int = Query(1, ge=0, description="Page number to retrieve, starting from 1. Use 0 to get all results."),
    size: int = Query(10, ge=0, le=100, description="Number of items per page (max 100). Use 0 to get all results.")
) -> MatchListResponse:
    """
    Retrieves paginated match fixtures for a given archive.

    Args:
        archiveId (str): The unique identifier of the archive to scrape matches from.
        page (int, optional): The page number to retrieve. Defaults to 1.
        size (int, optional): The number of items per page (maximum 100). Defaults to 10.

    Returns:
        MatchListResponse: A paginated list of match results.
    """
    try:
        logging.info(f"GET /{ROUTER_NAME}/{archiveId}/fixtures - Starting archive fixtures scraping process.")
        archive_scraper = ArchiveScraper()
        matches, pagination = archive_scraper.scrape_fixtures_by_archive(archiveId, page, size)

        logging.info(f"GET /{ROUTER_NAME}/{archiveId}/fixtures call successful - Fixtures of archive {archiveId} scraped.")
        return MatchListResponse(matches=matches, pagination=pagination)
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error occurred while processing fixtures for archive {archiveId}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{archiveId}/live", response_model=ListLiveMatch)
def get_live_by_archive(archiveId: str) -> ListLiveMatch:
    """
    Retrieves paginated match live for a given archive.

    Args:
        archiveId (str): The unique identifier of the archive to scrape matches from.
    Returns:
        MatchListResponse: List of live match.
    """
    try:
        logging.info(f"GET /{ROUTER_NAME}/{archiveId}/live - Starting live matches of archive {archiveId} scraping process.")
        archive_scraper = ArchiveScraper()
        matches = archive_scraper.scrape_live_by_archive(archiveId)

        logging.info(f"GET /{ROUTER_NAME}/{archiveId}/live call successful - Live matches of archive {archiveId} scraped.")
        return ListLiveMatch(matches=matches)
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error occurred while processing live matches for archive {archiveId}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{archiveId}/standings", response_model=StandingResponse)
def get_fixtures_by_archive(archiveId: str) -> StandingResponse:
    """
   Retrieves standings for a given archive.

   Args:
       archiveId (str): The unique identifier of the archive to scrape standings from.

   Returns:
       StandingResponse: The standings data for the archive.
   """
    try:
        logging.info(f"GET /{ROUTER_NAME}/{archiveId}/standings - Starting archive standings scraping process.")
        archive_scraper = ArchiveScraper()
        standings = archive_scraper.scrape_standings_by_archive(archiveId)

        logging.info(f"GET /{ROUTER_NAME}/{archiveId}/standings call successful - Standings of archive {archiveId} scraped.")
        return StandingResponse(standings=standings)
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error occurred while processing standings for archive {archiveId}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
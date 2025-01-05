import logging
from fastapi import APIRouter, HTTPException
from app.services.models.match_schemas import MatchResponse, MatchListResponse
from app.services.scraper.match_scraper import MatchScraper

ROUTER_NAME = 'matches'

router = APIRouter()

@router.get("/{matchId}", response_model=MatchResponse)
def get_match(matchId: str) -> MatchResponse:
    """
    Retrieves the match data by its ID.

    Args:
        matchId (str): The unique identifier of the match to scrape.

    Returns:
        MatchResponse: The scraped match data.
    """
    try:
        logging.info(f"GET /{ROUTER_NAME}/{matchId} - Starting match {matchId} scraping process.")
        match_scraper = MatchScraper()
        match = match_scraper.scrape_match(matchId)

        if match is None:
            logging.warning(f"Match with ID {matchId} not found.")
            raise HTTPException(status_code=404, detail=f"Match with ID {matchId} not found.")

        logging.info(f"GET /{ROUTER_NAME}/{matchId} call successful - Match {matchId} scraped.")
        return MatchResponse(match=match)
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error occurred while processing match {matchId}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch", response_model=MatchListResponse)
def get_matches(match_ids: list[str]) -> MatchListResponse:
    """
    Retrieves a list of matches based on the provided IDs.

    Args:
        match_ids (list[str]): A list of unique match identifiers to scrape.

    Returns:
        MatchListResponse: A list of scraped match data.
    """
    try:
        logging.info(f"POST /{ROUTER_NAME}/batch - Starting batch match scraping process for IDs: {match_ids}")
        match_scraper = MatchScraper()
        matches = []

        for match_id in match_ids:
            try:
                match = match_scraper.scrape_match(match_id)
                if match:
                    matches.append(match)
                else:
                    logging.warning(f"Match with ID {match_id} not found.")
            except Exception as e:
                logging.error(f"Error scraping match ID {match_id}: {e}")

        if not matches:
            logging.warning("No matches found for provided IDs.")
            raise HTTPException(status_code=404, detail="No matches found for provided IDs.")

        logging.info(f"POST /{ROUTER_NAME}/batch call successful - Matches scraped: {len(matches)}")
        return MatchListResponse(matches=matches)
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error occurred during batch match processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

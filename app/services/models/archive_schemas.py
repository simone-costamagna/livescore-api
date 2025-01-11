from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from app.services.models.utils import Pagination


class Match(BaseModel):
    id: str = Field(..., description="The unique identifier of the match")
    archive: str = Field(..., description="The unique identifier of the archive associated with the match")
    url: str = Field(..., description="The URL related to the match")
    match_date: datetime = Field(..., description="The date and time of the match")
    round: int = Field(..., description="The round number of the match")
    home: str = Field(..., description="The home team of the match")
    away: str = Field(..., description="The away team of the match")
    home_score: int = Field(0, description="The home team's score in the match")
    away_score: int = Field(0, description="The away team's score in the match")


class LiveMatch(BaseModel):
    id: str = Field(..., description="The unique identifier of the live match")
    archive: str = Field(..., description="The unique identifier of the archive associated with the live match")
    url: str = Field(..., description="The URL related to the live match")
    time: str = Field(..., description="The time of the live match")
    home: str = Field(..., description="The home team of the live match")
    away: str = Field(..., description="The away team of the live match")
    home_score: int = Field(0, description="The home team's score in the live match")
    away_score: int = Field(0, description="The away team's score in the live match")


class Archive(BaseModel):
    id: str = Field(..., description="The unique identifier of the archive")
    league: str = Field(..., description="The unique identifier of the league associated with the archive")
    season: str = Field(..., description="The season associated with the archive")
    url: str = Field(..., description="The URL related to the archive")
    live: str = Field(..., description="The URL for live scores of the archive")
    results: str = Field(..., description="The URL for results of the archive")
    fixtures: str = Field(..., description="The URL for fixtures of the archive")
    standings: str = Field(..., description="The URL for standings of the archive")

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name in {"league", "season"}:
            season = getattr(self, "season", "")
            league = getattr(self, "league", "")
            super().__setattr__("id", f"{league}-{season}")


class Rank(BaseModel):
    position: int = Field(..., description="The position of the team in the standings")
    team: str = Field(..., description="The name of the team")
    matches_played: int = Field(..., description="The number of matches played")
    wins: int = Field(0, description="The number of matches won")
    draws: int = Field(0, description="The number of matches drawn")
    losses: int = Field(0, description="The number of matches lost")
    goals_scored: int = Field(0, description="The number of goals scored")
    goals_conceded: int = Field(0, description="The number of goals conceded")
    points: int = Field(0, description="The total points accumulated")


class ArchiveResponse(BaseModel):
    archive: Archive


class MatchListResponse(BaseModel):
    matches: List[Match]
    pagination: Optional[Pagination] = Field(None, description="Pagination metadata")


class ListLiveMatch(BaseModel):
    matches: List[LiveMatch]


class StandingResponse(BaseModel):
    standings: List[Rank]

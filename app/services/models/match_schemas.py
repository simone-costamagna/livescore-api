from datetime import datetime
from typing import Tuple
from pydantic import BaseModel, Field


class Match(BaseModel):
    id: str = Field(default="", description="The id of the match")
    round: int = Field(default=0, description="The round of the match")
    match_date: datetime = Field(default=None, description="The date of the match")
    home: str = Field(default="", description="The home team of the match")
    away: str = Field(default="", description="The away team of the match")
    home_score: int = Field(default=0, description="The home score of the match")
    away_score: int = Field(default=0, description="The away score of the match")
    expected_goals_xg: Tuple[float, float] = Field(default=(None, None), description="The expected goals of the match")
    ball_possession: Tuple[int, int] = Field(default=(None, None), description="The ball possession of the match")
    goal_attempts: Tuple[int, int] = Field(default=(None, None), description="The goal attempts of the match")
    shots_on_goal: Tuple[int, int] = Field(default=(None, None), description="The shots on the goal of the match")
    shots_off_goal: Tuple[int, int] = Field(default=(None, None), description="The shots off the goal of the match")
    big_chances: Tuple[int, int] = Field(default=(None, None), description="The big chances of the match")
    corner_kicks: Tuple[int, int] = Field(default=(None, None), description="The corner kicks of the match")
    free_kicks: Tuple[int, int] = Field(default=(None, None), description="The free kicks of the match")
    offsides: Tuple[int, int] = Field(default=(None, None), description="The offsides of the match")
    fouls: Tuple[int, int] = Field(default=(None, None), description="The fouls of the match")
    yellow_cards: Tuple[int, int] = Field(default=(None, None), description="The yellow cards of the match")
    red_cards: Tuple[int, int] = Field(default=(None, None), description="The red cards of the match")


class MatchResponse(BaseModel):
    match: Match


class MatchListResponse(BaseModel):
    matches: list[Match]
from pydantic import BaseModel, Field
from typing import List, Any


class League(BaseModel):
    id: str = Field(None, description="The unique identifier of the league")
    country: str = Field(..., description="The name of the country")
    name: str = Field(..., description="The name of the league")
    url: str = Field(..., description="The URL related to the league")

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.id = f"{self.country}-{self.name}"



class Archive(BaseModel):
    id: str = Field(None, description="The unique identifier of the archive")
    league: str = Field(..., description="The unique identifier of the archive's league")
    season: str = Field(..., description="The season associated with the archive")
    url: str = Field(..., description="The URL related to the archive")
    winner: str = Field(None, description="The winner of the archive's season")

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.id = f"{self.league}-{self.season}"


class LeagueResponse(BaseModel):
    league: League


class ArchiveListResponse(BaseModel):
    archives: List[Archive]
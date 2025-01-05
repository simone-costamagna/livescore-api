from pydantic import BaseModel, Field
from typing import List, Any


class Country(BaseModel):
    id: str = Field(None, description="The unique identifier of the country", repr=False)
    name: str = Field(..., description="The name of the country")
    url: str = Field(..., description="The URL related to the country")

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.id = self.name


class League(BaseModel):
    id: str = Field(None, description="The unique identifier of the league", repr=False)
    country: str = Field(..., description="The name of the league's country")
    name: str = Field(..., description="The name of the league")
    url: str = Field(..., description="The URL related to the league")

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.id = f"{self.country}-{self.name}"


class CountryListResponse(BaseModel):
    countries: List[Country]


class LeagueListResponse(BaseModel):
    leagues: List[League]
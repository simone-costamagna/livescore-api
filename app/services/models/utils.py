from pydantic import BaseModel, Field

class Pagination(BaseModel):
    current_page: int = Field(..., description="The current page number.")
    page_size: int = Field(..., description="The number of items per page.")
    total_items: int = Field(..., description="The total number of items.")
    total_pages: int = Field(..., description="The total number of pages.")
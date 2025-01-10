from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ScraperModel(BaseModel):
    """Base model for scraper input and output"""

    id: Optional[str] = Field(None, description="MongoDB document ID")
    url: Optional[str] = Field(None, title="URL", description="URL to scrape")
    links: List[List[str]] = Field(
        default_factory=lambda: [[]], description="List of scraped links"
    )
    created_at: Optional[str] = Field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        description="Timestamp of when the data was scraped",
    )

    class Config:
        schema_extra = {
            "example": {
                "id": "678095a6c8127016357d8811",
                "url": "https://www.antaranews.com/terkini",
                "links": [
                    [
                        "https://www.antaranews.com/berita/4575238/example-article",
                        "https://www.antaranews.com/berita/4575246/another-article",
                    ]
                ],
                "created_at": "2025-01-10 10:36:06",
            }
        }


def ErrorResponseModel(error: str, code: int, message: str = "An error occurred"):
    return {"error": error, "code": code, "message": message}

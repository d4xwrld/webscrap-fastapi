from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ScraperModel(BaseModel):
    """Base model for scraper output"""

    links: List[List[str]] = Field(
        default_factory=lambda: [[]], description="List of scraped links"
    )

    class Config:
        schema_extra = {
            "example": {
                "links": [
                    [
                        "https://www.antaranews.com/berita/4575238/example-article",
                        "https://www.antaranews.com/berita/4575246/another-article",
                    ]
                ]
            }
        }


def ErrorResponseModel(error: str, code: int, message: str = "An error occurred"):
    return {"error": error, "code": code, "message": message}

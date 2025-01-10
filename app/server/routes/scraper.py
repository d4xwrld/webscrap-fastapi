from fastapi import APIRouter, HTTPException
from typing import List

from app.server.database import retrieve_scrapers, add_scraper
from app.server.models.scraper import ScraperModel

router = APIRouter()


@router.post("/", response_model=ScraperModel)
async def add_scraper_data(url: str):
    try:
        scraper = await add_scraper(url)
        return {
            "id": scraper["id"],
            "url": scraper["url"],
            "links": scraper.get("links", []),
            "created_at": scraper["created_at"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ScraperModel])
async def get_scrapers():
    try:
        scrapers = await retrieve_scrapers()
        if not scrapers:
            raise HTTPException(status_code=404, detail="No scrapers found")
        return scrapers  # Return the full scraper objects directly
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# bikin endpoint get baru buat hasil berita yang udah di scrape.

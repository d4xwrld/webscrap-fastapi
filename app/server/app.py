from fastapi import FastAPI
from app.server.routes.scraper import router as ScraperRouter

app = FastAPI()

app.include_router(ScraperRouter, tags=["Scraper"], prefix="/scraper")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}

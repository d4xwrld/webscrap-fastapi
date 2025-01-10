from requests_html import AsyncHTMLSession
from datetime import datetime
import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.scrapers
scraper_collection = database.get_collection("scraper_collection")


async def scrape_webpage(url: str) -> dict:
    session = AsyncHTMLSession()
    try:
        r = await session.get(url)
        await r.html.arender(sleep=1, scrolldown=10)  # For JavaScript rendered content

        # Get all links from the page
        title = r.html.find("h2.post_title, h2.post_title_medium", first=True)
        if not title:
            print("No title found")
        else:
            web_url = []
            # Find all 'a' tags and extract their href attributes
            for link in r.html.find("a"):
                if "href" in link.attrs:
                    # Convert relative URLs to absolute URLs
                    absolute_url = list(r.html.absolute_links)
                    # Only include links that contain "antaranews.com/berita/"
                    filtered_urls = [
                        url for url in absolute_url if "antaranews.com/berita/" in url
                    ]
                    if (
                        filtered_urls and filtered_urls not in web_url
                    ):  # Avoid duplicates
                        web_url.append(filtered_urls)
                    print(filtered_urls)
            return {
                "url": url,
                "links": web_url,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
    except Exception as e:
        raise Exception(f"Error scraping webpage: {str(e)}")
    finally:
        await session.close()


def scraper_helper(scraper: dict) -> dict:
    """Format scraper document into response schema with safe key access"""
    links = scraper.get("links", [[]])
    if not isinstance(links, list):
        links = [[]]
    elif links and not isinstance(links[0], list):
        links = [links]  # Wrap single list in outer list

    return {
        "id": str(scraper["_id"]),  # Convert ObjectId to string
        "url": scraper.get("url", ""),
        "links": links,
        "created_at": scraper.get(
            "created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ),
    }


async def add_scraper(url: str) -> dict:
    try:
        scraped_data = await scrape_webpage(url)

        # Ensure created_at exists
        if "created_at" not in scraped_data:
            scraped_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        scraper = await scraper_collection.insert_one(scraped_data)
        new_scraper = await scraper_collection.find_one({"_id": scraper.inserted_id})

        if not new_scraper:
            raise Exception("Failed to retrieve newly created scraper")

        return scraper_helper(new_scraper)  # Use helper to format response
    except Exception as e:
        raise Exception(f"Error adding scraper: {str(e)}")


# CRUD Operations
async def add_scraper(url: str) -> dict:
    try:
        scraped_data = await scrape_webpage(url)

        # Ensure created_at exists
        if "created_at" not in scraped_data:
            scraped_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        scraper = await scraper_collection.insert_one(scraped_data)
        new_scraper = await scraper_collection.find_one({"_id": scraper.inserted_id})

        if not new_scraper:
            raise Exception("Failed to retrieve newly created scraper")

        return scraper_helper(new_scraper)  # Use helper to format response
    except Exception as e:
        raise Exception(f"Error adding scraper: {str(e)}")
    try:
        # Scrape data from URL
        scraped_data = await scrape_webpage(url)

        # Ensure required fields exist
        if "created_at" not in scraped_data:
            scraped_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insert into database
        scraper = await scraper_collection.insert_one(scraped_data)

        # Get the newly created scraper
        new_scraper = await scraper_collection.find_one({"_id": scraper.inserted_id})
        if not new_scraper:
            raise Exception("Failed to retrieve newly created scraper")

        return scraper_helper(new_scraper)
    except Exception as e:
        raise Exception(f"Error adding scraper: {str(e)}")


async def retrieve_scrapers() -> list:
    try:
        scrapers = []
        async for scraper in scraper_collection.find():
            formatted_scraper = scraper_helper(scraper)
            # Ensure links is a list of lists
            if formatted_scraper["links"] and not isinstance(
                formatted_scraper["links"][0], list
            ):
                formatted_scraper["links"] = [formatted_scraper["links"]]
            scrapers.append(formatted_scraper)
        return scrapers
    except Exception as e:
        raise Exception(f"Error retrieving scrapers: {str(e)}")

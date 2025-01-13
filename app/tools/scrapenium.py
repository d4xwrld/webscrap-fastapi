from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
import os
import locale

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsScraper:
    def __init__(self):
        self.client = MongoClient("mongodb://127.0.0.1:27017/")
        self.db = self.client["scrapers"]
        self.collection = self.db["scraper_collection"]
        self.content_collection = self.db["scrapenium_collection"]
        self.setup_driver()

    def setup_driver(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        geckodriver_path = os.path.join(current_dir, "geckodriver")
        service = Service(geckodriver_path)
        self.driver = webdriver.Firefox(service=service, options=firefox_options)
        self.wait = WebDriverWait(self.driver, 10)

    def get_urls(self, document_id):
        document = self.collection.find_one({"_id": ObjectId(document_id)})
        if document and "links" in document:
            return document["links"][0] if document["links"] else []
        return []

    def scrape_article(self, url):
        try:
            self.driver.get(url)

            title = (
                self.wait.until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "wrap__article-detail-title")
                    )
                )
                .find_element(By.TAG_NAME, "h1")
                .text
            )

            locale.setlocale(locale.LC_TIME, "id_ID.UTF-8")
            date_element = self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "wrap__article-detail-info")
                )
            ).find_element(By.TAG_NAME, "span")
            date_text = date_element.text
            date_str = date_element.text.replace("WIB", "").strip()
            parsed_date = datetime.strptime(date_str, "%A, %d %B %Y %H:%M")

            content = self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "wrap__article-detail-content")
                )
            ).text

            data = {
                "url": url,
                "title": title,
                "date": parsed_date,
                "content": content,
                "scraped_at": datetime.now(),
            }

            self.content_collection.insert_one(data)
            logger.info(f"Scraped: {title}")
            return data

        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return None

    def close(self):
        if self.driver:
            self.driver.quit()


def main():
    scraper = NewsScraper()
    try:
        document_id = "6780b89a0876a4371fd73ead"
        urls = scraper.get_urls(document_id)
        logger.info(f"Found {len(urls)} URLs to process")

        for url in urls:
            result = scraper.scrape_article(url)
            if result:
                logger.info(f"Successfully saved article: {result['title']}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()

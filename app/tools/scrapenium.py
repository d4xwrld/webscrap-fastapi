from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
import logging
import os
import locale
from bs4 import BeautifulSoup
import requests

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsScraper:
    def __init__(self):
        mongo_url = os.getenv("MONGO_URL")
        self.client = MongoClient(mongo_url)
        self.db = self.client[os.getenv("MONGO_DB_NAME")]
        self.collection = self.db[os.getenv("MONGO_COLLECTION_NAME")]
        self.content_collection = self.db[os.getenv("MONGO_CONTENT_COLLECTION_NAME")]
        self.setup_driver()

    def setup_driver(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        geckodriver_path = os.path.join(current_dir, "geckodriver")
        service = Service(geckodriver_path)
        self.driver = webdriver.Firefox(service=service, options=firefox_options)
        self.wait = WebDriverWait(self.driver, 10)

    def get_urls(self):
        url = "https://www.antaranews.com/terkini/1"
        page = requests.get(url)
        scrap = BeautifulSoup(page.text, "html.parser")
        result = scrap.find_all("h2", class_="post_title post_title_medium")
        links = [item.find("a")["href"] for item in result if item.find("a")]
        logger.info(f"URLs to process: {links}")
        return links

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
            # date_text = date_element.text
            date_str = date_element.text.replace("WIB", "").strip()
            parsed_date = datetime.strptime(date_str, "%A, %d %B %Y %H:%M")

            content = self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "wrap__article-detail-content")
                )
            ).text

            author_element = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "p.text-muted.mt-2.small")
                )
            )
            author = author_element.text.split("\n")[0].replace("Pewarta: ", "")

            # author = self.wait.until(
            #     EC.presence_of_element_located(
            #         (By.CLASS_NAME, "wrap__article-detail-content").find_element(By.CSS_SELECTOR, "p.text-muted mt-2 small")
            #     )
            # )

            data = {
                "url": url,
                "title": title,
                "author": author,
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
        urls = scraper.get_urls()
        logger.info(f"Found {len(urls)} URLs to process")

        data = {
            "links": urls,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        document_id = scraper.collection.insert_one(data).inserted_id
        logger.info(f"Links inserted with document ID: {document_id}")

        for url in urls:
            result = scraper.scrape_article(url)
            if result:
                logger.info(f"Successfully saved article: {result['title']}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()

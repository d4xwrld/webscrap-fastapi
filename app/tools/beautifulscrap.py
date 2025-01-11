from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
from datetime import datetime

# from bson.objectid import ObjectId
url = "https://www.antaranews.com/terkini/"

page = requests.get(url)

# Connect to MongoDB
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["beautifulscrap"]

scrap = BeautifulSoup(page.text, "html")
result = scrap.find_all("h2", class_="post_title post_title_medium")
links = [item.find("a")["href"] for item in result if item.find("a")]
print(f"URLs to process: {links}")

content_collection = db["links"]

if not result:
    print("artikelnya gada")
else:
    data = {
        "link": links,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    content_collection.insert_one(data)
    print(f"Data inserted: {data}")

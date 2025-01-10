from requests_html import HTMLSession
from pymongo import MongoClient
from bson.objectid import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["scrapers"]
collection = db["scraper_collection"]
document_id = "6780b89a0876a4371fd73ead"
session = HTMLSession()
urls = []
document = collection.find_one({"_id": ObjectId(document_id)})
if document and "links" in document:
    urls = document["links"][0] if document["links"] else urls
print(f"URLs to process: {urls}")

# Create a new collection for storing the content
content_collection = db["test_collection"]

for url in urls:
    if not url:
        continue

    try:
        r = session.get(url)
        r.html.render(sleep=1, scrolldown=3, timeout=30)
        articles = r.html.find("div.wrap__article-detail")
    except Exception as e:
        print(f"Error loading page {url}: {str(e)}")
        continue

    if not articles:
        print("artikelnya gada")
    else:
        for item in articles:
            try:
                title = (
                    item.find("h1", first=True).text
                    if item.find("h1", first=True)
                    else "No title"
                )

                newsitem_author = item.find("p.text-muted.mt-2.small", first=True)
                name = (
                    newsitem_author.text.split("Pewarta:")[1]
                    .split("Editor:")[0]
                    .strip()
                    if newsitem_author and "Pewarta:" in newsitem_author.text
                    else "No author"
                )

                newsitem_p = item.find("p")
                newsitem_date = item.find(
                    "span.text-secondary.font-weight-normal", first=True
                )

                if newsitem_p:
                    links = []
                    for p in newsitem_p:
                        if p.absolute_links:
                            links.extend(list(p.absolute_links))

                    data = {
                        "source_url": url,
                        "title": title,
                        "author": name,
                        "date": newsitem_date.text if newsitem_date else "No date",
                        "content": " ".join(p.text for p in newsitem_p),
                        "links": links,
                    }

                    result = content_collection.insert_one(data)
                    print(f"Saved content with ID: {result.inserted_id}")
                    print(f"Data saved: {data}")
                else:
                    print("No paragraphs found")
            except Exception as e:
                print(f"Error processing article from {url}: {str(e)}")

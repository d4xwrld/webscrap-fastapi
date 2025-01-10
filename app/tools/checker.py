from pymongo import MongoClient
from bson.objectid import ObjectId

# Connect to MongoDB using the exact connection string from your setup
client = MongoClient("mongodb://127.0.0.1:27017/")

# Access the database and collection we see in the image
db = client["scrapers"]  # The database containing the scraper_collection
collection = db["scraper_collection"]  # The collection we see in the image

# Query for the document using ObjectId
document_id = "6780b89a0876a4371fd73ead"
try:
    document = collection.find_one({"_id": ObjectId(document_id)})
    if document:
        print(document)
    else:
        print("Document not found.")
except Exception as e:
    print(f"An error occurred: {e}")

# Close the connection
client.close()

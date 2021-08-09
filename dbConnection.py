import os
from pymongo import MongoClient
import gridfs

keyString = os.environ.get("MONGO_KEY") 

client = MongoClient(keyString)
print('Connected to DB')
db = client["aerialweb"]
collection = db["search-cache"]
fs = gridfs.GridFS(db)

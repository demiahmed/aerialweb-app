import os
from pymongo import MongoClient
import gridfs

# get env variables
keyString = os.environ.get("MONGO_KEY") 

client = MongoClient("mongodb+srv://admin:aerialweb@aerialweb.rtttv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['aerialweb']
fs = gridfs.GridFS(db)
print('Connected to DB')

imagePath = 'static/images/'
files = os.listdir(imagePath)

# for file in files:
#     # print(file)
#     image = open(imagePath+file, "rb")
#     data = image.read()
#     fs.put(data, filename=file)
#     print(f"{files.index(file)+1} of {len(files)} complete")
#     # break


# Get value from DB gives as bytestring

name = "S2A_MSIL2A_20190819T031541_N0213_R118_T48NUG_20190819T091330.jpg"
res = db.fs.files.find_one({"filename": name})
my_id = res["_id"]
import base64
out = base64.b64encode(fs.get(my_id).read())
# out = fs.get(my_id).read()
print(out[:500])


# Test to see if actual S2 linkicoon is rendered as bytestring

# import requests
# i = "https://scihub.copernicus.eu/dhus/odata/v1/Products('8eb78c3f-59f4-4ec7-9a92-ba97e870338c')/Products('Quicklook')/$value"
# r = requests.get(i, auth=('demi12395', "Sutd1234"))
# print(r.content)




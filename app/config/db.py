
from pymongo import MongoClient


uri = "mongodb+srv://hao123:hao123@mongodb.txxq6.mongodb.net/?retryWrites=true&w=majority&appName=Mongodb"
# Create a new client and connect to the server
cluster = MongoClient(uri)


db = cluster['face_ekyc']
collection = db['users']
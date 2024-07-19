from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

url = "mongodb+srv://alfisha23catax:Alfisha%40123@cluster0.a6fdu8s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(url, server_api=ServerApi('1'))
db = client.coflex

admin = db["admins_data"]


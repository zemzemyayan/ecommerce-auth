# mongo.py
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
mongo_db = client["ecommerce"]

cart_collection = mongo_db["carts"]
product_collection = mongo_db["products"]

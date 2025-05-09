# test_insert_cart.py
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
db = client["ecommerce"]
carts = db["carts"]

cart_data = {
    "user_id": 1,  # Bu kullanıcı ID'si MySQL tarafındaki auth tablosundan geliyor olabilir
    "items": [
        {
            "product_id": "663a30e6123456789abcde00",  # product koleksiyonundaki _id (örnek)
            "name": "Mouse",
            "quantity": 2,
            "price": 150
        },
        {
            "product_id": "663a30e6123456789abcde01",
            "name": "Klavye",
            "quantity": 1,
            "price": 300
        }
    ],
    "total_price": 600,
    "created_at": datetime.utcnow()
}

result = carts.insert_one(cart_data)
print("Sepet eklendi, ID:", result.inserted_id)

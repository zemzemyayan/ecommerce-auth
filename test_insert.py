from mongo import product_collection

product = {
    "_id": "abc123",
    "name": "Ayakkabı",
    "price": 299.99,
    "supplier_id": 1
}

product_collection.insert_one(product)
print("Ürün eklendi.")

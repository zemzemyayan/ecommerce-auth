# product/routes.py

from flask import Blueprint, request, jsonify
from bson import ObjectId
from mongo import product_collection, cart_collection
from middleware.auth_required import token_required

product_bp = Blueprint("product", __name__)

# Ürün ekleme (sadece supplier)
@product_bp.route('/product', methods=['POST'])
@token_required(role='supplier')
def add_product(current_user):
    data = request.get_json()
    product = {
        "_id": data["product_id"],
        "name": data["name"],
        "price": data["price"],
        "supplier_id": current_user["user_id"],
        "deleted": False
    }
    product_collection.insert_one(product)
    return jsonify({"message": "Ürün eklendi"}), 201

# Ürünleri listele (sadece aktif ürünler)
@product_bp.route('/product', methods=['GET'])
@token_required()
def list_products(current_user):
    products = product_collection.find({"deleted": False})
    result = []
    for p in products:
        result.append({
            "product_id": p["_id"],
            "name": p["name"],
            "price": p["price"]
        })
    return jsonify(result), 200

# Ürün güncelleme (sadece supplier)
@product_bp.route('/product/<product_id>', methods=['PUT'])
@token_required(role='supplier')
def update_product(current_user, product_id):
    data = request.get_json()
    update_data = {}
    if "name" in data:
        update_data["name"] = data["name"]
    if "price" in data:
        update_data["price"] = data["price"]

    result = product_collection.update_one(
        {"_id": product_id, "supplier_id": current_user["user_id"]},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        return jsonify({"message": "Ürün bulunamadı veya yetkisiz"}), 404

    return jsonify({"message": "Ürün güncellendi"}), 200

# Ürün silme (soft delete) (sadece supplier)
@product_bp.route('/product/<product_id>', methods=['DELETE'])
@token_required(role='supplier')
def delete_product(current_user, product_id):
    product = product_collection.find_one({"_id": product_id, "supplier_id": current_user["user_id"]})
    if not product:
        return jsonify({"message": "Ürün bulunamadı veya yetkisiz"}), 404

    # Soft delete
    product_collection.update_one({"_id": product_id}, {"$set": {"deleted": True}})

    # Kullanıcı sepetinde varsa işaretle (bilgi amaçlı, sepette 'silinmiş' işaretiyle gözüksün)
    cart_collection.update_many(
        {"items.product_id": product_id},
        {"$set": {"items.$[elem].deleted": True}},
        array_filters=[{"elem.product_id": product_id}]
    )

    return jsonify({"message": "Ürün silindi (soft-delete)"}), 200

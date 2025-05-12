from flask import Blueprint, request, jsonify
from pymongo import MongoClient

from bson import ObjectId

from mongo import client  # varsayılan mongo bağlantın burada

from db import get_user_by_id  # MySQL'den kullanıcı doğrulama işlemi için
from flask_jwt_extended import jwt_required, get_jwt_identity



cart_bp = Blueprint("cart", __name__)
db = client["ecommerce"]
carts = db["carts"]
products = db["products"]

#Sepeti Oluştur (ilk ürün eklenirken oluşur)
@cart_bp.route("/cart/add", methods=["POST"])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()

    data = request.get_json()
    print("Gelen JSON verisi:", data)  # DEBUG LOG
    if not data:
        return jsonify({"msg": "Geçersiz JSON verisi"}), 400

    _id = data.get("_id")
    try:
        quantity = int(data.get("quantity", 1))
    except (ValueError, TypeError):
        return jsonify({"msg": "quantity sayısal olmalı"}), 422

    if not _id:
        return jsonify({"msg": "_id eksik"}), 422

    # Ürün var mı?
    product = products.find_one({"_id": _id, "deleted": False})
    if not product:
        return jsonify({"msg": "Ürün bulunamadı"}), 404

    # Sepet kontrolü
    cart = carts.find_one({"user_id": user_id})
    if not cart:
        new_cart = {
            "user_id": user_id,
            "items": [{"_id": _id, "quantity": quantity}]
        }
        carts.insert_one(new_cart)
        return jsonify({"msg": "Sepet oluşturuldu ve ürün eklendi"}), 201
    else:
        items = cart["items"]
        for item in items:
            if item["_id"] == _id:
                item["quantity"] += quantity
                break
        else:
            items.append({"_id": _id, "quantity": quantity})

        carts.update_one({"user_id": user_id}, {"$set": {"items": items}})
        return jsonify({"msg": "Ürün sepete eklendi"}), 200


# Sepeti Listele (ürün detaylarıyla)
@cart_bp.route("/cart", methods=["GET"])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    cart = carts.find_one({"user_id": user_id})

    if not cart or not cart.get("items"):
        return jsonify({"msg": "Sepet boş"}), 200

    detailed_items = []
    for item in cart["items"]:
        product = products.find_one({"_id": item["_id"], "deleted": False})
        if product:
            detailed_items.append({
                "_id": item["_id"],
                "name": product["name"],
                "price": product["price"],
                "supplier_id": product["supplier_id"],
                "quantity": item["quantity"]
            })

    return jsonify({"cart": detailed_items}), 200


#Ürün Adedini Güncelle
@cart_bp.route("/cart/update", methods=["PUT"])
@jwt_required()
def update_cart_item():
    user_id = get_jwt_identity()
    data = request.get_json()
    _id = data.get("_id")
    quantity = int(data.get("quantity"))

    if quantity < 1:
        return jsonify({"msg": "Miktar en az 1 olmalıdır"}), 400

    cart = carts.find_one({"user_id": user_id})
    if not cart:
        return jsonify({"msg": "Sepet bulunamadı"}), 404

    updated = False
    for item in cart["items"]:
        if item["_id"] == _id:
            item["quantity"] = quantity
            updated = True
            break

    if not updated:
        return jsonify({"msg": "Ürün sepette yok"}), 404

    carts.update_one({"user_id": user_id}, {"$set": {"items": cart["items"]}})
    return jsonify({"msg": "Ürün miktarı güncellendi"}), 200


#Sepetten Ürün Sil
@cart_bp.route("/cart/remove", methods=["DELETE"])
@jwt_required()
def remove_from_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    _id = data.get("_id")

    cart = carts.find_one({"user_id": user_id})
    if not cart:
        return jsonify({"msg": "Sepet bulunamadı"}), 404

    new_items = [item for item in cart["items"] if item["_id"] != _id]

    carts.update_one({"user_id": user_id}, {"$set": {"items": new_items}})
    return jsonify({"msg": "Ürün sepetten silindi"}), 200

#Sepeti Temizle
@cart_bp.route("/cart/clear", methods=["DELETE"])
@jwt_required()
def clear_cart():
    user_id = get_jwt_identity()
    carts.update_one({"user_id": user_id}, {"$set": {"items": []}})
    return jsonify({"msg": "Sepet temizlendi"}), 200

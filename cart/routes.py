#crud işlemleri burda yapılacak
# cart/routes.py
from flask import Blueprint, request, jsonify
from mongo import cart_collection, product_collection
from middleware.auth_required import token_required
cart_bp = Blueprint("cart", __name__)


@cart_bp.route('/cart/add', methods=['POST'])
@token_required()
def add_to_cart(current_user):
    user_id = current_user['user_id']
    data = request.get_json()
    product_id = data['product_id']
    quantity = data.get('quantity', 1)

    cart = cart_collection.find_one({"user_id": user_id})

    if not cart:
        new_cart = {
            "user_id": user_id,
            "items": [{"product_id": product_id, "quantity": quantity}]
        }
        cart_collection.insert_one(new_cart)
    else:
        # Eğer ürün zaten sepette varsa, miktarını artır
        for item in cart['items']:
            if item['product_id'] == product_id:
                item['quantity'] += quantity
                break
        else:
            cart['items'].append({"product_id": product_id, "quantity": quantity})

        cart_collection.update_one(
            {"user_id": user_id},
            {"$set": {"items": cart['items']}}
        )

    return jsonify({"message": "Ürün sepete eklendi"}), 200

@cart_bp.route('/cart', methods=['GET'])
@token_required()
def get_cart(current_user):
    user_id = current_user['user_id']
    cart = cart_collection.find_one({"user_id": user_id})

    if not cart:
        return jsonify({"message": "Sepet boş"}), 200

    return jsonify(cart), 200

@cart_bp.route('/cart', methods=['GET'])
@token_required()
def get_cart(current_user):
    user_id = current_user['user_id']
    cart = cart_collection.find_one({"user_id": user_id})

    if not cart:
        return jsonify({"message": "Sepet boş"}), 200

    return jsonify(cart), 200

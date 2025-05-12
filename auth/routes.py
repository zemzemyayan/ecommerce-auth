# auth/routes.py
from flask import Blueprint, request, jsonify
from db import get_connection
from auth.utils import hash_password, check_password, create_token
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from auth.utils import check_password


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data['email']
    password = data['password']
    role = data['role']

    conn = get_connection()
    cursor = conn.cursor()
    hashed = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (email, password, role) VALUES (%s, %s, %s)",
                       (email, hashed, role))
        conn.commit()
        return jsonify({"message": "Kayıt başarılı!"}), 201
    except:
        return jsonify({"message": "Kayıt başarısız!"}), 400


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user and check_password(password, user['password']):
        # ID'yi string'e çeviriyoruz
        access_token = create_access_token(identity=str(user['id']))
        return jsonify({"access_token": access_token}), 200

    return jsonify({"message": "Geçersiz giriş"}), 401

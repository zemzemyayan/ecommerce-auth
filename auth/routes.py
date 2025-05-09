# auth/routes.py
from flask import Blueprint, request, jsonify
from db import get_connection
from auth.utils import hash_password, check_password, create_token

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
    data = request.json
    email = data['email']
    password = data['password']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user and check_password(password, user['password']):
        token = create_token(user['id'], user['role'])
        return jsonify({"token": token})
    return jsonify({"message": "Geçersiz giriş"}), 401

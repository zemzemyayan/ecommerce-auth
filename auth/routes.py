# auth/routes.py
import datetime
from datetime import timedelta
from flask_jwt_extended import decode_token
from flask import Blueprint, request, jsonify
from db import get_connection
from auth.utils import hash_password, check_password, create_token
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
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

#Şifremi Unuttum Fonksiyonu
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({'msg': 'Kullanıcı bulunamadı'}), 404

    # Token üret
    reset_token = create_access_token(identity=str(user['id']), expires_delta=datetime.timedelta(minutes=15))


    # Şifre sıfırlama linki oluştur
    reset_link = f"http://localhost:5000/reset-password/{reset_token}"

    # Burada e-posta gönderme işlemi yapılmalı (SMTP veya Mail API)
    print(f"\n\n*** Şifre sıfırlama linki: {reset_link}\n\n")  # Şimdilik terminale yaz

    return jsonify({'msg': 'Şifre sıfırlama bağlantısı e-posta adresinize gönderildi.'}), 200


#şifre sıfırlama
@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    try:
        #user_id = get_jwt_identity()
        decoded_token = decode_token(token)
        user_id = int(decoded_token['sub'])  # 'sub' alanı, identity bilgisi

    except Exception as e:
        print("Token decode hatası:", e)
        return jsonify({"msg": "Geçersiz veya süresi dolmuş token"}), 401

    data = request.get_json()
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({'msg': 'Yeni şifre gerekli'}), 400

    hashed_pw = hash_password(new_password)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password=%s WHERE id=%s", (hashed_pw, user_id))
    conn.commit()
    return jsonify({'msg': 'Şifre başarıyla güncellendi'}), 200
#Not:Şu an e-posta gönderimi yapamıyorsan, print() ile terminale link basmak yeterli olur.

# Profil Güncelleme
@auth_bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    conn = get_connection()
    cursor = conn.cursor()

    # Şifre güncelleniyorsa hashle
    if password:
        password = hash_password(password)
        cursor.execute(
            "UPDATE users SET email=%s, password=%s WHERE id=%s",
            (email, password, user_id)
        )
    else:
        cursor.execute(
            "UPDATE users SET  email=%s WHERE id=%s",
            (email, user_id)
        )

    conn.commit()
    return jsonify({"msg": "Profil başarıyla güncellendi"}), 200

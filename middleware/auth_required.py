# middleware/auth_required.py
from functools import wraps
from flask import request, jsonify
import jwt
from config import SECRET_KEY


def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = None
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

            if not token:
                return jsonify({"message": "Token gerekli!"}), 401

            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                if role and data.get("role") != role:
                    return jsonify({"message": "Yetkisiz erişim"}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token süresi dolmuş"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Geçersiz token"}), 403

            return f(current_user=data, *args, **kwargs)
        return wrapper
    return decorator

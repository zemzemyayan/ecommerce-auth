# JWT doğrulama decorator'u
# middleware/auth_required.py
from functools import wraps
from flask import request, jsonify
import jwt
from config import SECRET_KEY

def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"message": "Token gerekli!"}), 401

            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                if role and data.get('role') != role:
                    return jsonify({"message": "Yetkisiz erişim"}), 403
                return f(current_user=data, *args, **kwargs)
            except:
                return jsonify({"message": "Geçersiz token"}), 403
        return wrapper
    return decorator

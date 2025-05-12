# app.py
from flask import Flask, jsonify

import config
from auth.routes import auth_bp
from middleware.auth_required import token_required
from flask_jwt_extended import JWTManager
from config import JWT_SECRET_KEY  # config.py dosyasındaki JWT_SECRET_KEY'yi alıyoruz
app = Flask(__name__)
# JWT için yapılandırmayı Flask uygulamasına ekliyoruz
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
jwt = JWTManager(app)


app.register_blueprint(auth_bp, url_prefix='/auth')

from product.routes import product_bp
app.register_blueprint(product_bp)

from cart.routes import cart_bp
app.register_blueprint(cart_bp, url_prefix='/api')


@app.route('/')
def home():
    return jsonify({"message": "API aktif!"})

@app.route('/dashboard')
@token_required()
def dashboard(current_user):
    return jsonify({"message": f"Hoş geldin kullanıcı {current_user['user_id']}", "role": current_user['role']})

@app.route('/supplier-only')
@token_required(role='supplier')
def only_supplier(current_user):
    return jsonify({"message": f"Tedarikçi özel erişim verildi, kullanıcı ID: {current_user['user_id']}"})

if __name__ == '__main__':
    app.run(debug=True)

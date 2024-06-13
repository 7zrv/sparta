from flask import Blueprint, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from model import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"message": "로그인 성공"}), 200
    return jsonify({"message": "로그인 실패"}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "로그아웃 성공"}), 200

@auth_bp.route('/current_user', methods=['GET'])
@login_required
def get_current_user():
    return jsonify({"email": current_user.email, "nickname": current_user.nickname}), 200

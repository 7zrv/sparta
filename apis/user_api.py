from flask import Blueprint, request, jsonify
from model import User
from app import db

user_bp = Blueprint('user', __name__, url_prefix='/api')

@user_bp.route('/user', methods=['POST'])
def register_user():
    data = request.json
    nickname = data.get('nickname')
    email = data.get('email')
    password = data.get('password')
    phone_number = data.get('phone_number')

    if not all([nickname, email, password, phone_number]):
        return jsonify({"error": "Missing required fields"}), 400

    new_user = User(nickname=nickname, email=email, password=password, phone_number=phone_number)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@user_bp.route('/user', methods=['GET'])
def users_info():

    users = User.query.all()

    user_list = []

    for user in users:
        user_data = {
            'user_id': user.user_id,
            'nickname': user.nickname,
            'email': user.email,
            'phone_number': user.phone_number
        }
        user_list.append(user_data)


    return jsonify({"users": user_list}), 200



@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_userInfo(user_id):

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user_info = {
        "nickname": user.nickname,
        "email": user.email,
        "phone_number": user.phone_number,
    }

    return jsonify(user_info), 200

from werkzeug.security import generate_password_hash

@user_bp.route('/user/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    data = request.json
    nickname = data.get('nickname')
    email = data.get('email')
    password = data.get('password')
    phone_number = data.get('phone_number')

    if not any([nickname, email, password, phone_number]):
        return jsonify({"error": "No update information provided"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if nickname:
        user.nickname = nickname
    if email:
        user.email = email
    if password:
        user.password = generate_password_hash(password)
    if phone_number:
        user.phone_number = phone_number

    db.session.commit()

    return jsonify({"message": "User updated successfully"}), 200


@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
def user_secession(user_id):

    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "user secession successfully"}), 200



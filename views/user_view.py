from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from model import User, Book
from db import db

user_bp = Blueprint('users', __name__)

@user_bp.route('/user/register_user', methods=['POST'])
def register_user():

    nickname = request.form['nickname']
    email = request.form['email']
    password = request.form['password']
    phone_number = request.form['phone_number']


    if not all([nickname, email, password, phone_number]):
        return jsonify({"error": "Incomplete user information"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(nickname=nickname, email=email, password=password, phone_number=phone_number)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('books.get_users'))

@user_bp.route('/user/login', methods=['POST'])
def login():

    email = request.form['email']
    password = request.form['password']
    print(email, password)
    if not all([email, password]):
        return jsonify({"error": "Incomplete user information"}), 400
    
    find_user = User.query.filter(User.email == email, User.password == password).first()

    if not find_user:
        return jsonify({"error": "email or password is incorrect."}), 400
    
    return redirect(url_for('books.get_users', user_id=find_user.user_id))

@user_bp.route('/user/<int:user_id>', methods=['POST'])
def update_user(user_id):

    nickname = request.form['nickname']
    email = request.form['email']
    password = request.form['password']
    phone_number = request.form['phone_number']

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
        user.password = password
    if phone_number:
        user.phone_number = phone_number

    db.session.commit()

    return redirect(url_for('books.get_users'))
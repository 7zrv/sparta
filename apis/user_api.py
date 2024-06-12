from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from model import User
from app import db

user_api = Blueprint('user_api', __name__)

# 회원가입 라우트
@user_api.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        nickname = request.form['nickname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        phone_number = request.form['phone_number']

        if password != confirm_password:
            return "Password and Confirm Password do not match"

        # 비밀번호 해싱
        hashed_password = generate_password_hash(password)

        new_user = User(username=username, nickname=nickname, email=email, phone_number=phone_number, password_hash=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "Error in adding user"
    return render_template('register.html')

# 회원정보 조회 라우트
@user_api.route('/user/<int:id>')
def user_detail(id):
    user = User.query.get_or_404(id)
    return render_template('user_detail.html', user=user)

# 회원정보 수정 라우트
@user_api.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.nickname = request.form['nickname']
        user.email = request.form['email']
        user.phone_number = request.form['phone_number']
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "Error in updating user"
    return render_template('edit_user.html', user=user)

# 회원정보 삭제 라우트
@user_api.route('/delete/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "Error in deleting user"

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# 현재 디렉토리 경로
basedir = os.path.abspath(os.path.dirname(__file__))

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy 객체 생성
db = SQLAlchemy(app)

# 모델 정의


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    


# 기본 라우트


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

# 회원가입 라우트


@app.route('/register', methods=['GET', 'POST'])
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


@app.route('/user/<int:id>')
def user_detail(id):
    user = User.query.get_or_404(id)
    return render_template('user_detail.html', user=user)

# 회원정보 수정 라우트


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
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


@app.route('/delete/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "Error in deleting user"


if __name__ == '__main__':
    # 데이터베이스 초기화 (최초 실행 시 한 번만 필요)
    with app.app_context():
        db.create_all()
    app.run(debug=True)

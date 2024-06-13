from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from db import db


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # renamed to _password
    phone_number = db.Column(db.String(20), nullable=False)
    books = db.relationship('Book', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.nickname}>'

    def check_password(self, password):
        return self.password == password

    def get_id(self):
        return str(self.user_id)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    book_info = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    rental = db.Column(db.Boolean, default=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

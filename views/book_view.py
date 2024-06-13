from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from model import Book, User
from db import db

book_view_bp = Blueprint('book_view', __name__)

@book_view_bp.route('/books')
def get_users():
    user_id = request.args.get("user_id", "")
    
    context = {
        "user": ""
    }

    if not user_id:
        return render_template('books.html', context=context)
    
    find_user = User.query.filter_by(user_id=user_id).first()

    if not find_user:
        return render_template('books.html', context=context)
    
    user_data = find_user.serialize()

    context['user'] = user_data

    return render_template('books.html', context=context)


@book_view_bp.route('/books/create/<int:user_id>', methods=['POST'])
def book_create(user_id):
    
    title = request.form['title']
    author = request.form['author']
    book_info = request.form['book_info']
    subject = request.form['subject']
    img_url = request.form['img_url']

    if not all([title, author, book_info, subject, user_id, img_url]):
        return jsonify({"error": "Incomplete book information"}), 400

    new_book = Book(title=title, author=author, book_info=book_info, subject=subject, user_id=user_id, img_url=img_url)

    db.session.add(new_book)
    db.session.commit()

    return redirect(url_for('book_view.get_users', user_id=user_id))

@book_view_bp.route('/books/search/<int:user_id>', methods=['POST'])
def book_search(user_id):

    find_user = User.query.filter_by(user_id=user_id).first()
    filter_book_title = request.form['title']

    if not all([filter_book_title]):
        return jsonify({"error": "Incomplete book information"}), 400

    find_book = Book.query.filter_by(user_id=user_id, title=filter_book_title).all()

    if not find_book:
        return jsonify({"error": "Not exisit"}), 400
    
    user_data = find_user.serialize()
    user_data['books'] = [book.serialize() for book in find_book]

    context = {
        'user': user_data
    }
    return render_template('books.html', context=context)
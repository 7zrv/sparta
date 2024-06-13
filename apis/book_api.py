from flask import Blueprint, request, jsonify
from model import Book
from app import db

book_bp = Blueprint('book', __name__, url_prefix='/api')


@book_bp.route('/book', methods=['POST'])
def create_book():

    data = request.json
    title = data.get('title')
    author = data.get('author')
    book_info = data.get('book_info')
    subject = data.get('subject')
    rental = data.get('rental')
    user_id = data.get('user_id')
    img_url = data.get('img_url')

    if not all([title, author, book_info, subject, rental, user_id, img_url]):
        return jsonify({"error": "Incomplete book information"}), 400

    new_book = Book(title=title, author=author, book_info=book_info, subject=subject, rental=rental, user_id=user_id, img_url=img_url)

    db.session.add(new_book)
    db.session.commit()

    return jsonify({"message": "Book created successfully"}), 201


@book_bp.route('/book', methods=['GET'])
def book_info():

    books = Book.query.all()

    book_list = []

    for book in books:
        book_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'book_info': book.book_info,
            'subject': book.subject,
            'user_id': book.user_id,
            'img_url': book.img_url
        }
        book_list.append(book_data)


    return jsonify({"books": book_list}), 200


@book_bp.route('/book/<int:book_id>', methods=['PATCH'])
def book_info_change(book_id):

    data = request.json
    title = data.get('title')
    author = data.get('author')
    book_info = data.get('book_info')
    subject = data.get('subject')
    rental = data.get('rental')
    user_id = data.get('user_id')
    img_url = data.get('img_url')


    if not any([title, author, book_info, subject, rental, user_id, img_url]):
        return jsonify({"error": "변경된 점이 없습니다."}), 400


    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Data not found"}), 404

    if title:
        book.title = title
    if author:
        book.author = author
    if book_info:
        book.book_info = book_info
    if subject:
        book.subject = subject
    if rental is not None:
        book.rental = rental
    if user_id:
        book.user_id = user_id
    if img_url:
        book.img_url = img_url

    db.session.commit()

    return jsonify({"message": "Book updated successfully"}), 200

@book_bp.route('/book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted successfully"}), 200


@book_bp.route('/book/rent/<int:book_id>', methods=['PATCH'])
def book_rent(book_id):
    book = Book.query.get(book_id)

    if not book:
        return jsonify({"error": "Data not found"}), 404

    book.rental = not book.rental

    db.session.commit()

    return jsonify({"message": "Book updated successfully"}), 200
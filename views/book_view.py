from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from model import Book, User

book_bp = Blueprint('books', __name__)


@book_bp.route('/books', methods=['GET'])
def get_users():
    user_id = request.args.get("user_id", "")
    
    context = {
        "user": "",
    }
    if not user_id:
        return render_template('books.html', context=context)
    
    user = User.query.filter_by(user_id=user_id).first().serialize()
    print(user)

    context['user'] = user

    return render_template('books.html', context=context)

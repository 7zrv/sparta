from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from model import Book, User

book_view_bp = Blueprint('book_view', __name__)

@book_view_bp.route('/books')
def get_users():
    user_id = request.args.get("user_id", "")
    
    context = {
        "user": "",
    }

    if not user_id:
        return render_template('books.html', context=context)
    
    find_user = User.query.filter_by(user_id=user_id).first()

    if not find_user:
        return render_template('books.html', context=context)
    
    user_data = find_user.serialize()
    print(user_data)

    context['user'] = user_data

    return render_template('books.html', context=context)

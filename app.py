# app.py
from flask import Flask, render_template
from db import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Replace with your actual secret key
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # views
    from views import main_views
    app.register_blueprint(main_views.bp)

    from views import book_view
    app.register_blueprint(book_view.book_view_bp)

    from views import user_view
    app.register_blueprint(user_view.user_view_bp)

    # apis
    from apis import book_api
    app.register_blueprint(book_api.book_bp)

    from apis import user_api
    app.register_blueprint(user_api.user_bp)

    @app.route("/")
    def home():
        return render_template('index.html')

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

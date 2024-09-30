from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from models import User, Task  # Import User and Task models inside the function

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # This needs to be defined here after User is imported

    from routes import main_routes
    app.register_blueprint(main_routes)

    with app.app_context():
        db.create_all()

    return app

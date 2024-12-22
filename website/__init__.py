from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
# LoginManager me permite controlar las sessiones, al igual que PHP.

import os  # Para el uso de variables de entorno


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    # debo decirle a donde redirecciona si la session no existe o se termina jejeje. Para los sitios que la requieran,.
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # como el id es mi clave primaria debo indicarlo
        return User.query.get(int(id))

    return app


def create_database(app):
    with app.app_context():  # Entra en el contexto de la aplicación
        db.create_all()  # Crea todas las tablas

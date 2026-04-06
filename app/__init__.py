from flask import Flask, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = "Por favor, inicia sesión para acceder."

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super-secret-retro-key-1985'
    
    # Base de datos local SQLite para entorno offline
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'retro_gaming.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    # Inyectar traducciones globales
    from .i18n import get_translation
    @app.context_processor
    def inject_translations():
        lang = session.get('lang', 'es')
        return dict(_=lambda key: get_translation(lang, key), current_lang=lang)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    from .routes import main as main_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    return app

import os

from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder="views", static_folder="static")

    #config authentification par passkey
    load_dotenv()
    app.secret_key = os.environ.get("FLASK_SECRET_KEY")

    # Charge le fichier .env à la racine du projet
    ROOT_DIR = Path(__file__).resolve().parents[1]
    load_dotenv(ROOT_DIR / ".env")

    #config bdd avec variables d'environnement
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    #prend le schéma Vote
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {
            "options": '-c search_path="Vote"',
            "connect_timeout": 5
        }
    }

    #lie l'orm à l'application
    db.init_app(app)


    #import des routes
    from .routes.routes import bp
    app.register_blueprint(bp)

    return app
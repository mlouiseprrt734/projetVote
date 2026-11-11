import os

from dotenv import load_dotenv
from flask import Flask

def create_app():
    app = Flask(__name__, template_folder="views", static_folder="static")

    #config authentification par passkey
    load_dotenv()
    app.secret_key = os.environ.get("FLASK_SECRET_KEY")

    from .routes.routes import bp
    app.register_blueprint(bp)

    return app
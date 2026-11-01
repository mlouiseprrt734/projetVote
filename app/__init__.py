import os

from flask import Flask

def create_app():
    app = Flask(__name__, template_folder="views", static_folder="static")

    #config authentification par passkey
    app.secret_key = os.urandom(32)   # signs the Flask session cookie

    from .routes.routes import bp
    app.register_blueprint(bp)

    return app
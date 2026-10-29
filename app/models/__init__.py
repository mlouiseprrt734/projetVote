from flask import Flask

def create_app():
    app = Flask(__name__, template_folder="views", static_folder="static")

    from .routes.routes import bp
    app.register_blueprint(bp)

    return app
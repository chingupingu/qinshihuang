from flask import Flask
from flask_cors import CORS

def create_app(config=None):
    app = Flask(__name__)
    CORS(app)
    if config:
        app.config.update(config)
    with app.app_context():
        from .routes import register_routes
        register_routes(app)
    return app
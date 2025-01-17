# the controller of the backend
# contains the endpoints to call certain functions

from flask import Flask, request, jsonify
from flask_cors import CORS
from app.routes import register_routes

app = Flask(__name__)
CORS(app)
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
"""
App starting point.
"""
from api_routes import api_routes
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(api_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)

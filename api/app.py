from flask import Flask
from db import Db as db
app = Flask(__name__)
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

import api_routes


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=5001)
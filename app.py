from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

subreddits = [   'Bodyswap',
    'FemalePossession',
    'animalswap',
    'AnimePossession',
    'BodySwapRP',
    'CelebSwap',
    'MinorityBodySwap',
    'FictionBodySwap',
]

@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html", subreddits=subreddits)


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
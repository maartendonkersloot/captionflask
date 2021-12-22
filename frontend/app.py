"""
Index app routes/main
"""
from flask import Flask, render_template
from flask_cors import CORS
from config import get_api_key

app = Flask(__name__)
CORS(app)

subreddits = [
    "Bodyswap",
    "FemalePossession",
    "animalswap",
    "AnimePossession",
    "BodySwapRP",
    "CelebSwap",
    "MinorityBodySwap",
    "FictionBodySwap",
]


@app.route("/")
def hello_world():
    """
    Index route
    Returns:
        [type]: index template
    """
    key = get_api_key()
    return render_template("index.html", subreddits=subreddits, api=key)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

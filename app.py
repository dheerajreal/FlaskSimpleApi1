from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy(app)


@app.route("/", methods=["GET"])
def index():
    return "hello"


@app.route("/", methods=["POST"])
def post():
    return "hello"


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

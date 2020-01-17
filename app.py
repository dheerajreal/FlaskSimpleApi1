from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_pyfile("config.py")


@app.errorhandler(404)
def error_404(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(405)
def error_405(error):
    return make_response(jsonify({'error': 'Not Allowed'}), 405)


class Posts(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    content = db.Column(db.String())

    def __repr__(self):
        return f"{self.id}=>{self.name}"


@app.route("/", methods=["GET"])
def index():
    posts = Posts.query.all()
    data = {}
    for post in posts:
        data[post.id] = {"name": post.name, "content": post.content}

    return jsonify(data)


@app.route("/", methods=["POST"])
def create():
    data = request.json
    name = data["name"]
    content = data["content"]
    post = Posts(name=name, content=content)

    db.session.add(post)
    db.session.commit()
    return jsonify({"Response": "successfully created"})


@app.route("/<int:id>", methods=["GET"])
def read(id):
    post = Posts.query.get_or_404(id)
    data = {"name": post.name, "content": post.content}
    return jsonify({"Response": data})


@app.route("/<int:id>", methods=["PUT"])
def update(id):
    post = Posts.query.get_or_404(id)
    data = request.json
    name = data["name"]
    content = data["content"]
    post.name = name
    post.content = content
    db.session.commit()

    data = {"name": post.name, "content": post.content}
    return jsonify({"Response": data})


@app.route("/<int:id>", methods=["DELETE"])
def delete(id):
    post = Posts.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()

    return jsonify({"Response": "successfully deleted"})


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

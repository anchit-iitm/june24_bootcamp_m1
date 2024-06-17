from flask import Flask, jsonify

from config import LocalDev
from database.models import db, user_datastore
from app_security import security

def create_app():

    app = Flask(__name__)
    app.config.from_object(LocalDev)

    db.init_app(app)

    security.init_app(app, user_datastore)
    return app

app = create_app()

@app.route("/hello_world")
def hello_world():
    return jsonify({"message": "Hello, World!"})

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
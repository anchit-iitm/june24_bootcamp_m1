from flask import Flask, jsonify, request
from flask_security import verify_password
from flask_restful import Api

from config import LocalDev
from database.models import db, user_datastore
from app_security import security

# app = Flask(__name__)
# app.config.from_object(LocalDev)
# db.init_app(app)
# security.init_app(app, user_datastore)

def create_app():

    app = Flask(__name__)
    app.config.from_object(LocalDev)

    db.init_app(app)

    security.init_app(app, user_datastore)

    api = Api(app)

    return app, api

app, api_handler = create_app()

@app.route("/hello_world/<int:var2>", methods=["GET", "POST", "PUT", "DELETE"])
def hello_world(var2):
    return jsonify({"message": "Hello, World!", "data": var2})

@app.route('/login', methods=['POST'])
def login_():
    data = request.get_json()
    # email = data.get('email')
    email = data['email']
    password = data['password']
    user = user_datastore.find_user(email=email)
    if user:
        if verify_password(password, user.password):
            token = user.get_auth_token()
            return jsonify({'token': token, 'email': user.email})
        return jsonify({'message': 'password doesnt match'}), 401
    return jsonify({'message': 'user not present'}), 401


from routes.auth import hello, login
api_handler.add_resource(hello, '/api/hello_world/<int:var2>')
api_handler.add_resource(login, '/api/login')

from routes.category import CategoryResource, CategorySpecific
api_handler.add_resource(CategoryResource, '/api/category')
api_handler.add_resource(CategorySpecific, '/api/category/<int:id>')

with app.app_context():
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    if not user_datastore.find_user(email='admin@a.com'):
        user_datastore.create_user(email='admin@a.com', password='admin', roles=['admin'])
        
    db.session.commit()

if __name__ == "__main__":
    app.run()
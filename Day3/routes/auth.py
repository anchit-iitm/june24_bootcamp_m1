from flask_restful import Resource
from flask import jsonify, request, make_response
from flask_security import verify_password, login_user

from database.models import user_datastore, db

class hello(Resource):
    def post(self, var2):
        return jsonify({"message": "Hello, World!", "data": var2})

    def get(self):
        return jsonify({"message": "Hello, World!"})

    def put(self):
        return jsonify({"message": "Hello, World! put"})

    def delete(self):
        return jsonify({"message": "Hello, World!"})
    
class login(Resource):
    def post(self):
        data = request.get_json()
        # email = data.get('email')
        email = data['email']
        password = data['password']
        print(email, password)
        user = user_datastore.find_user(email=email)
        if user:
            if verify_password(password, user.password):
                login_user(user)
                db.session.commit()
                token = user.get_auth_token()
                return make_response(jsonify({'token': token, 'email': user.email}), 200)
            return make_response(jsonify({'message': 'password doesnt match', 'password': password}), 401)
        return make_response(jsonify({'message': 'user not present', 'email': email}), 401)
from app import create_app
from database.models import db, user_datastore
from flask import request
from flask_security import roles_accepted, current_user, verify_password

import atexit

def empty_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database emptied")

atexit.register(empty_db)

def temp_db():
    with app.app_context():
        db.create_all()
        print("Database created")
        user_datastore.find_or_create_role(name='admin', description='Administrator')
        user_datastore.find_or_create_role(name='user', description='User')
        if not user_datastore.find_user(email='admin@a.com'):
            user_datastore.create_user(email='admin@a.com', password='admin', roles=['admin'])
        if not user_datastore.find_user(email='user@a.com'):
            user_datastore.create_user(email='user@a.com', password='user', roles=['user'])
        db.session.commit()
        print("User created")

app = create_app()

temp_db()

@app.route("/test1", methods=["POST"])
def test1():
    data = request.get_json()
    user = user_datastore.find_user(email=data["email"])
    if user and verify_password(data["password"], user.password):
        return {"message": "login success", "user": user.email, "token": user.get_auth_token()}
    else:
        return {"message": "login failed"}
@app.route("/test2")
@roles_accepted("admin")
def test2():
    return {"message": "admin only", "user": current_user.email}

@app.route("/test3")
@roles_accepted("user")
def test3():
    return {"message": "public", "user": current_user.email}

@app.route("/test4", methods=["POST"])
def test4():
    data = request.get_json()
    if not user_datastore.find_user(email=data["email"]):
        user = user_datastore.create_user(email=data["email"], password=data["password"], roles=['user'])
        db.session.commit()
        return {"message": "user created", "user": user.email}

if __name__ == "__main__":
    app.run()
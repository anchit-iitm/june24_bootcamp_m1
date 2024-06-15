from flask import Flask, render_template, jsonify, make_response
from flask_security import Security, SQLAlchemyUserDatastore, current_user, roles_accepted, auth_token_required
import os 
# from config import DevConfig
from database.models import db, User, Role

app = Flask(__name__)

# app.config.from_object(DevConfig)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_TRACKABLE'] = True
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authorization'
    # Generate a nice key using secrets.token_urlsafe()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw') 
    # Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
    # Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')


user_datastore=SQLAlchemyUserDatastore(db, User, Role)
security=Security(app, user_datastore)


# db=sqlalchemy(app)
db.init_app(app)

with app.app_context():
    db.create_all()
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='user', description='End user')
    db.session.commit()
    # User.query.filter_by(email='admin@a.com').first()
    if not user_datastore.find_user(email='admin@a.com'):
        user_datastore.create_user(email='admin@a.com', password='admin', roles=['admin'])
        db.session.commit()
    if not User.query.filter_by(username='test1').first():
        test_user = user_datastore.create_user(username='test1', password='test1', active=False)
        user_datastore.add_role_to_user(test_user, 'user')
        db.session.commit()
    

@app.route('/token')
def token():
    user1 = user_datastore.find_user(email='admin@a.com')
    token = user1.get_auth_token()
    return jsonify({'token': token, 'email': user1.email})

@app.route('/token1')
def token1():
    user1 = user_datastore.find_user(username='test1')
    user1.active = True
    db.session.commit()
    token = user1.get_auth_token()
    return jsonify({'token': token, 'email': user1.username})


@app.route('/hello_world', methods=['POST'])
# @auth_token_required
# @roles_accepted('admin')
def hello_world():
    print(current_user.id)
    return jsonify({'message': 'Hello, World!', 'user': current_user.username, 'email': current_user.email})
    # return current_user.username

@app.route('/')
def index():
    var1 = 'my app' #user1
    var3 = 1 #token
    return render_template('index.html', var2=var1,var4=var3)

if __name__ == '__main__':
    app.run()

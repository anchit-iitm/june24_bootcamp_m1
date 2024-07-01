from flask import Flask, jsonify, request
from flask_security import verify_password
from flask_restful import Api
from flask_cors import CORS # type: ignore
 
from config import LocalDev
from database.models import db, user_datastore
from app_security import security

# app = Flask(__name__)
# app.config.from_object(LocalDev)
# db.init_app(app)
# security.init_app(app, user_datastore)

def make_celery(app):
    import celeryconfig
    from celery import Celery
    celery = Celery(app.import_name) # celery = Celery(app)
    celery.config_from_object(celeryconfig)
    return celery

def create_app():
    from caching import cache
    from mailer import mail

    app = Flask(__name__)
    app.config.from_object(LocalDev)

    db.init_app(app)

    security.init_app(app, user_datastore)

    api = Api(app)

    CORS(app)

    cache.init_app(app)

    celery = make_celery(app)

    mail.init_app(app)

    return app, api, celery

app, api_handler, celery_app = create_app()
import tasks

from celery.schedules import crontab
celery_app.conf.beat_schedule = {
    'var1': {
        'task': 'tasks.add',
        'schedule': crontab(minute=16, hour=6, day_of_month=1)
    }, 
    # 'var2': {
    #     'task': 'tasks.helloWorld',
    #     'schedule': 2.0
    # },
    'var3': {
        'task': 'tasks.cate_query',
        'schedule': crontab(minute=17, hour=6)
    },
    'var4': {
        'task': 'tasks.mail_test',
        'schedule': crontab(minute=31, hour=6)
    },
    'var5': {
        'task': 'tasks.ex_daily',
        'schedule': crontab(minute=43, hour=6)
    },
}

@app.route('/celery')
def celery_test():
    tasks.helloWorld.delay()
    tasks.add.delay()
    tasks.cate_query.delay()
    return jsonify({"message": "Hello, World!"})

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


from routes.auth import hello, login, register
api_handler.add_resource(hello, '/api/hello_world/<int:var2>')
api_handler.add_resource(login, '/api/login')
api_handler.add_resource(register, '/api/register')

from routes.category import CategoryResource, CategorySpecific
api_handler.add_resource(CategoryResource, '/api/category')
api_handler.add_resource(CategorySpecific, '/api/category/<int:id>')

from routes.product import ProductResource, ProductSpecific
api_handler.add_resource(ProductResource, '/api/product')
api_handler.add_resource(ProductSpecific, '/api/product/<int:id>')

from routes.admin import CategoryDelete, ProductDelete, toggle_user_status, UserResources
api_handler.add_resource(CategoryDelete, '/api/category_delete/<int:id>')
api_handler.add_resource(ProductDelete, '/api/product_delete/<int:id>')
api_handler.add_resource(toggle_user_status, '/api/toggle_user_status/<int:id>')
api_handler.add_resource(UserResources, '/api/users', '/api/user/<int:id>')

from routes.celery_route import dailyMail
api_handler.add_resource(dailyMail, '/api/celery/test')

with app.app_context():
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    if not user_datastore.find_user(email='admin@a.com'):
        user_datastore.create_user(email='admin@a.com', password='admin', roles=['admin'])
        
    db.session.commit()

if __name__ == "__main__":
    app.run()
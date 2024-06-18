from app import create_app
from database.models import db, user_datastore
app, api_handler = create_app()

with app.app_context():
    db.drop_all()
    print("Dropped all tables")

    db.create_all()
    print("Created all tables")

    user_datastore.find_or_create_role(name='admin', description='Administrator')
    print("Created role admin")
    user_datastore.find_or_create_role(name='manager', description='Store manager')
    print("Created role manager")
    user_datastore.find_or_create_role(name='customer', description='Store customer')
    print("Created role customer")

    if not user_datastore.find_user(email='admin@a.com'):
        user_datastore.create_user(email='admin@a.com', password='admin', roles=['admin', 'manager', 'customer'])
        print("Created admin user")
    if not user_datastore.find_user(email='manager@a.com'):
        user = user_datastore.create_user(email='manager@a.com', password='manager')
        user_datastore.add_role_to_user(user, 'manager')
        user_datastore.add_role_to_user(user, 'customer')
        print("Created manager user")

    if not user_datastore.find_user(email='customer@a.com'):
        user = user_datastore.create_user(email='customer@a.com', password='customer')
        user_datastore.add_role_to_user(user, 'customer')
        print("Created customer user")

    db.session.commit()
    
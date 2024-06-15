import os
from datetime import timedelta, datetime

# Define a base configuration class
class Config():
    # Turn off debug mode by default
    DEBUG = False
    # Set the SQLite database directory to None by default
    SQLITE_DB_DIR = None
    # Set the SQLAlchemy database URI to None by default
    SQLALCHEMY_DATABASE_URI = None
    # Turn off SQLAlchemy's event system, which can consume a lot of resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    # SECURITY_REGISTERABLE = True
    # SECURITY_JOIN_USER_ROLES = True
    SECURITY_TRACKABLE = True
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'
    # Generate a nice key using secrets.token_urlsafe()
    SECRET_KEY = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw') 
    # Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
    # Generate a good salt using: secrets.SystemRandom().getrandbits(128)
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')

    SQLALCHEMY_TRACK_MODIFICATIONS = False




import os
from datetime import timedelta
from dotenv import load_dotenv

from ..database import BASE_DIR

load_dotenv()

class Config:
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=1)
    JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY")

class DevConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='sqlite:///'+ os.path.join(BASE_DIR, 'db.sqlite3')    # uri for sqllite 3
    # SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI')           # uri for other databases
    SQLALCHEMY_TRACK_MODIFICATIONS=False


class TestConfig(Config):
    TESTING=True
    SQLALCHEMY_ECHO=True  
    SQLALCHEMY_DATABASE_URI='sqlite://'  
    SQLALCHEMY_TRACK_MODIFICATIONS=False


class ProdConfig(Config):
    pass

config_dict={
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}


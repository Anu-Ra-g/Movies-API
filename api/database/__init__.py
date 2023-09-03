from flask_sqlalchemy import SQLAlchemy
import os

BASE_DIR=os.path.dirname(os.path.realpath(__file__))

db = SQLAlchemy()  


from api import db

class User(db.Model):
    
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(355), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()
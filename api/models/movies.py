from api import db

class Movie(db.Model):

    __tablename__= 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    imdb_score = db.Column(db.Float, nullable=False)
    popularity = db.Column(db.Float, nullable=False)
    
    genres = db.relationship('Genre', backref='movie', lazy=True, cascade='all, delete-orphan')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Genre(db.Model):

    __tablename__= 'genres'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(50), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'), nullable=False)
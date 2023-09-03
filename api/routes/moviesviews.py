from flask_restx import Namespace, Resource, fields, abort
from http import HTTPStatus
from flask import request
from flask_jwt_extended import jwt_required


from ..models.movies import Movie, Genre
from ..database import db

movies_namespace=Namespace('movies',description="Definitions for Movies routes")

movie_model=movies_namespace.model(
    'Movie',{
        'id': fields.Integer(description="Id for movies"),
        'name': fields.String(description="Name of movie", required=True),
        'director': fields.String(description="Name of the director", required=True),
        'popularity': fields.Float(description="Popularity score", required=True),
        'imdb_score': fields.Float(description="IMdb score", required=True),
        'genres': fields.List(fields.String(description="Genre of the movie"), description="Genres of the movies", required=True),
    }
)


@movies_namespace.route('/allmovies')
class GetAllMovies(Resource):

    @movies_namespace.marshal_list_with(movie_model)
    @movies_namespace.doc(description="Retrieve all the movies")
    def get(self):
        """
            Get all the movies
        """
        query = Movie.query

        director_filter = request.args.get('director')
        genre_filter = request.args.get('genre')
        name_filter = request.args.get('name')
        imdb_score_filter = request.args.get('imdb_score')

        if director_filter:
            query = query.filter(Movie.director == director_filter)
        if genre_filter:
            query = query.join(Genre).filter(Genre.genre == genre_filter)
        if name_filter:
            query = query.filter(Movie.name == name_filter)
        if imdb_score_filter:
            query = query.filter(Movie.imdb_score == float(imdb_score_filter))

        movies = query.all()

        movies_with_genres = []

        for movie in movies:
            movie_data = {
                'id': movie.id,
                'name': movie.name,
                'director': movie.director,
                'popularity': movie.popularity,
                'imdb_score': movie.imdb_score,
                'genres': [genre.genre for genre in movie.genres]
            }
            movies_with_genres.append(movie_data)

        return movies_with_genres, HTTPStatus.OK

    
@movies_namespace.route('/movie')
class CreateAMovie(Resource):

    @movies_namespace.expect(movie_model, validate=True)
    @movies_namespace.doc(description="Create a new movie")
    @jwt_required()
    def post(self):
        """
            Create a new movie
        """

        data=request.get_json()

        existing_movie=Movie.query.filter(
            Movie.name == data['name'],
            Movie.director == data['director']
        ).first()

        if existing_movie:
            abort(HTTPStatus.CONFLICT, message="Movie with same name and director already exists")

        new_movie = Movie(
            name=data['name'],
            director=data['director'],
            popularity=data['popularity'],
            imdb_score=data['imdb_score']
        )

        for genre_name in data['genres']:
            genre = Genre(genre=genre_name)
            new_movie.genres.append(genre)
        
        new_movie.save()

        created_movie_data = {
            'id': new_movie.id,
            'name': new_movie.name,
            'director': new_movie.director,
            'popularity': new_movie.popularity,
            'imdb_score': new_movie.imdb_score,
            'genres': [genre.genre for genre in new_movie.genres]
        }

        return created_movie_data, HTTPStatus.CREATED
    

@movies_namespace.route('/movie/<int:movie_id>')
class CRUDMoviesById(Resource):

    
    @movies_namespace.marshal_with(movie_model)
    @movies_namespace.doc(
        description="Retrieve a movie by ID",
         params={
            "movie_id": "An Id for a given movie"
        }
    )
    @jwt_required()
    def get(self, movie_id):
        """
            Retrieve a movie by id
        """
        
        data=Movie.query.get_or_404(movie_id)

        created_movie_data = {
            'id': data.id,
            'name': data.name,
            'director': data.director,
            'popularity': data.popularity,
            'imdb_score': data.imdb_score,
            'genres': [genre.genre for genre in data.genres]
        }

        return created_movie_data, HTTPStatus.OK

    @movies_namespace.expect(movie_model, validate=True)
    @movies_namespace.doc(
        description="Update a movie by ID",
         params={
            "movie_id": "An Id for a given movie"
        }
    )
    @jwt_required()    
    def put(self, movie_id):
        """
            Update a movie by id
        """

        data=Movie.query.get_or_404(movie_id)

        updatemovie=request.get_json()

        data.popularity = updatemovie['popularity']
        data.director = updatemovie['director']
        data.imdb_score = updatemovie['imdb_score']
        data.name = updatemovie['name']

        new_genres = updatemovie['genres']

        for genre in data.genres:
            db.session.delete(genre)

        for genre_name in new_genres:
            genre = Genre(genre=genre_name, movie_id=data.id)  
            db.session.add(genre)

        db.session.commit()

        return {"message": f"Updated movie with id {data.id}"}, HTTPStatus.OK

    @movies_namespace.doc(
        description="Update an order by ID",
         params={
            "movie_id": "An Id for a given movie"
        }
    )
    @jwt_required()  
    def delete(self, movie_id):
        """
            Delete a movie by id
        """

        data=Movie.query.get_or_404(movie_id)

        data.delete()

        return {"message": f"Delete movie with id {data.id}"}, HTTPStatus.OK


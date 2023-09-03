from flask import Flask
from flask_restx import Api, Resource
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed


from .config.config import config_dict
from .database import db
from .routes.authviews import auth_namespace   
from .routes.moviesviews import movies_namespace

# database tables are created here
from .models.users import User    
from .models.movies import Movie


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config) 

    db.init_app(app)

    with app.app_context():
        db.create_all()

    jwt_manager = JWTManager(app)

    authorizations = {
    "Bearer Auth": {  # Use "Bearer Auth" as the security scheme name
        "type": "apiKey",  # Correct the type to "apiKey"
        "in": "header",    # Use "header" instead of "Header"
        "name": "Authorization",
        "description": "Add a JWT with **Bearer <JWT>** to authorize."
        }
    }


    api = Api(app,
            title="Movies API",
            description="A REST API for a movies database",
            authorizations=authorizations,
            security="Bearer Auth"
    )

    api.add_namespace(movies_namespace, path='/movies')
    api.add_namespace(auth_namespace, path='/auth')

    @api.errorhandler(NotFound)
    def not_found(error):
        print("error here")
        return {"error": "Not Found"}, 404

    @api.errorhandler(MethodNotAllowed)
    def methods_not_allowed(error):
        print("error here")
        return {"error": "Method Not allowed"}, 405
    
    @api.route('/<path:invalid_path>')
    class CatchAll(Resource):
        def get(self, invalid_path):
            return {"error": "Not Found", "message": f"No endpoint matched for {invalid_path}"}, 404
        
    return app
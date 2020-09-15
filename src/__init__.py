from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from .movies.service import GenreService, MovieService, MoviesService
from . import movies
from .constants import BASE_URL
from .auth import auth_bp
from .config import Config

jwt = JWTManager


def create_app(config = Config):
    app = Flask(__name__)
    app.config.from_object(config)
    create_api(app)
    jwt.init_app(app)
    app.register_blueprint(auth_bp)
    return app


def create_api(app):
    api = Api(app, prefix=BASE_URL)
    api.add_resource(MoviesService, movies.MOVIES_ENDPOINT)
    api.add_resource(MovieService, movies.MOVIE_ENDPOINT)
    api.add_resource(GenreService, movies.GENRE_ENDPOINT)
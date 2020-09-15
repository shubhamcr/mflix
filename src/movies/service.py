from flask import request, abort
from flask_restful import Resource
from marshmallow import Schema, fields
from bson import ObjectId
from . import db
from ..constants import BASE_URL_WITHOUT_SLASH


def get_paginated_response(start, limit, base_url, sort_key):
    result = {}
    count = db.get_movies_count()
    if count < start:
        abort(404)

    result["start"] = start
    result["limit"] = limit
    result["total_movies"] = count

    if start == 1:
        result["previous"] = ""
    else:
        new_start = max(1, start - limit)
        new_limit = min(limit, start - 1)
        result["previous"] = base_url + "?start=%d&limit=%d" % (new_start, new_limit)

    if start+limit > count:
        result["next"] = ""
    else:
        new_start = start + limit
        new_limit = min(limit, count - (start+limit) + 1)
        result["next"] = base_url + "?start=%d&limit=%d" % (new_start, new_limit)

    return result, db.get_movies(start, limit, sort_key)


class MoviesSchema(Schema):
    start = fields.Integer(required=True)
    limit = fields.Integer(required=True)


class MoviesService(Resource):
    def get(self):
        start = request.args.get("start", 1)
        limit = request.args.get("limit", 20)
        try:
            start = int(start)
            limit = int(limit)
        except ValueError:
            abort(404, "start and limit must be convertible to integer.")
        schema = MoviesSchema()
        errors = schema.validate({"start": start, "limit": limit})
        if errors:
            abort(400, str(errors))
        result, movies = get_paginated_response(
            start=start, limit=limit, base_url=request.base_url, sort_key="imdb.rating")
        for movie in movies:
            movie["movie_url"] = request.url_root + BASE_URL_WITHOUT_SLASH + "/movie/" + str(movie["_id"])
            del movie["_id"]

        result["movies"] = movies
        return result


class MovieService(Resource):
    def get(self, id):
        movie_id = ObjectId(id)
        movie = db.get_movie_by_id(movie_id)
        if "_id" in movie:
            del movie["_id"]
        return movie


class GenreService(Resource):
    def get(self):
        genre = request.args.get("genre")
        if not genre:
            abort(404, "Genre query parameter cannot be empty.")
        movies = db.filter_movies(filter={"genres": {"$eq": genre}})
        for movie in movies:
            if movie["_id"]:
                del movie["_id"]
        result = {
            "count": len(movies),
            "movies": movies
        }
        return result

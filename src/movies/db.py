from pymongo import MongoClient

db = MongoClient("mongodb+srv://analytics:analytics-password@mflix-mnkxv.mongodb.net/mflix?retryWrites=true&w="
                     "majority")["mflix"]


def get_movies(start, limit, sort_key):
    movies = db.movies.find().sort(sort_key, -1).skip(start-1).limit(limit)
    return list(movies)


def get_movies_count():
    return db.movies.count_documents({})


def get_movie_by_id(id):
    return db.movies.find_one({"_id": id})


def filter_movies(filter):
    movie_cursor = db.movies.find(filter)
    result = [movie for movie in movie_cursor]
    return result
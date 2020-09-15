from pymongo import MongoClient

db = MongoClient("mongodb+srv://analytics:analytics-password@mflix-mnkxv.mongodb.net/mflix?retryWrites=true&w="
                     "majority")["mflix"]


def username_exists(username):
    return db.user.count_documents({"username": username}, limit = 1)


def create_user(username, password, name):
    result = db.user.insert_one(
        {
            "username": username,
            "password": password,
            "name": name
        })
    return result.inserted_id


def authenticate_user(username, password):
    return db.user.find_one({
        "username": username,
        "password": password
    })


from . import mongo


def get_user(username):
    user = mongo.db.users.find_one({'username': username})
    return user


def add_user(contact_data):
    mongo.db.users.insert_one({'username': contact_data['username'],
                               'password': contact_data['password']})

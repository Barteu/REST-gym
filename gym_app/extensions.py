from flask_sqlalchemy import SQLAlchemy
import hashlib

db = SQLAlchemy()


def hash_tup(tup):
    string = ''
    for item in tup:
        string = string + str(item)

    hash_object  = hashlib.md5(string.encode())
    return hash_object.hexdigest()


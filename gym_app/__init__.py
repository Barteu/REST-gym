from flask import Flask
from flask_restful import Api

from gym_app.extensions import db

from gym_app.resources.todo import Todo, TodoList
from gym_app.resources.gym import Gym, GymList

def create_app():
    app = Flask(__name__)

    from flask_sqlalchemy import SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

    db.init_app(app)
    db.app = app
    return app


app = create_app()

api = Api(app)

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(GymList, '/gyms')
api.add_resource(Gym, '/gyms/<gym_id>')


from gym_app import models

from flask import Flask
from flask_restful import reqparse, Api

from gym_app.resources.todo import Todo, TodoList

app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('task')

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')



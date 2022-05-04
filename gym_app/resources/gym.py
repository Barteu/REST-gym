from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from gym_app.models import GymModel
from gym_app import db
from flask import jsonify, make_response
import json, dataclasses

parser = reqparse.RequestParser()
parser.add_argument('name')

def abort_if_gym_doesnt_exist(gym_id):
    if GymModel.query.filter(GymModel.id == int(gym_id)).first() is None:
        abort(404, message="Gym {} doesn't exist".format(gym_id))


class Gym(Resource):
    def get(self, gym_id):
        abort_if_gym_doesnt_exist(gym_id)
        gym = GymModel.query.filter(GymModel.id == int(gym_id)).first()

        response = make_response(jsonify(gym))
        response.status_code = 200
        response.headers['etag'] = hash(gym)
        return response


    def put(self, gym_id):
        args = parser.parse_args()
        abort_if_gym_doesnt_exist(gym_id)
        gym = GymModel.query.filter(GymModel.id == int(gym_id)).first()
        if args['name'] is not None:
            gym.name = args['name']
        db.session.commit()

        response = make_response(jsonify(gym))
        response.status_code = 200
        response.headers['etag'] = hash(gym)

        return response

    def patch(self, gym_id):
        args = parser.parse_args()
        abort_if_gym_doesnt_exist(gym_id)
        gym = GymModel.query.filter(GymModel.id == int(gym_id)).first()
        if args['name'] is not None:
            gym.name = args['name']
        db.session.commit()

        response = make_response(jsonify(gym))
        response.status_code = 200
        response.headers['etag'] = hash(gym)

        return response

        
    def delete(self, gym_id):
        abort_if_gym_doesnt_exist(gym_id)

        try:
             GymModel.query.filter(GymModel.id == int(gym_id)).delete()
             db.session.commit()
             return 204 
        except: 
             return 404
        


class GymList(Resource):
    def get(self):
        gyms = GymModel.query.all()
        response = make_response(jsonify(gyms))
        response.status_code = 200
        return response

    def post(self):
        args = parser.parse_args()
        gym = GymModel(name=args['name'])
        db.session.add(gym)
        db.session.commit()

        response = make_response(jsonify(gym))
        response.status_code = 201
        response.headers['etag'] = hash(gym)
        return response


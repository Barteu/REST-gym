from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from gym_app.models import GymModel
from gym_app import db
from flask import jsonify, make_response
import json, dataclasses


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('If-None-Match', location='headers')


def abort_if_gym_doesnt_exist(gym_id):
    gym =  GymModel.query.filter(GymModel.id == int(gym_id)).first()
    if gym is None:
        abort(404, message="Gym {} doesn't exist".format(gym_id))
    else:
        return gym


def abort_if_etag_doesnt_match(etag, res_etag):
    if etag is None or res_etag != etag.replace('"',''):
        abort(412, message="ETag doesn't match")


class Gym(Resource):
    def get(self, gym_id):
       
        gym = abort_if_gym_doesnt_exist(gym_id)
     
        response = make_response(jsonify(gym))
        response.status_code = 200

        response.headers['ETag'] = gym.get_hash()
        return response


    def put(self, gym_id):
        args = parser.parse_args()
        gym = abort_if_gym_doesnt_exist(gym_id)
      
        abort_if_etag_doesnt_match(args['If-None-Match'], gym.get_hash())

        if args['name'] is not None:
            gym.name = args['name']

        try:
            db.session.commit()
        except:
            return 404

        response = make_response(jsonify(gym))
        response.status_code = 200
        response.headers['ETag'] = gym.get_hash()

        return response


    def patch(self, gym_id):
        args = parser.parse_args()
        gym = abort_if_gym_doesnt_exist(gym_id)

        abort_if_etag_doesnt_match(args['If-None-Match'], gym.get_hash())

        if args['name'] is not None:
            gym.name = args['name']
        try:
            db.session.commit()
        except:
            return 404

        response = make_response(jsonify(gym))
        response.status_code = 200
        response.headers['ETag'] = gym.get_hash()

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
        try:
            db.session.add(gym)
            db.session.commit()
        except:
            return 404

        response = make_response(jsonify(gym))
        response.status_code = 201
        response.headers['ETag'] = gym.get_hash()
        return response


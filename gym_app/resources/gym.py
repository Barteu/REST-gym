from email import message
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource, url_for
from gym_app.models import GymModel, EquipmentModel, EquipmentAffiliationModel
from gym_app import db
from flask import jsonify, make_response
from gym_app.utils import abort_if_limit_or_offset_is_bad, abort_if_etag_doesnt_match

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('location')
parser.add_argument('If-None-Match', location='headers')



def abort_if_gym_doesnt_exist(gym_id):
    gym =  GymModel.query.filter(GymModel.id == int(gym_id)).first()
    if gym is None:
        abort(404, message="Gym {} doesn't exist".format(gym_id))
    else:
        return gym


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
        if args['location'] is not None:
            gym.location = args['location']
        try:
            gym.check_completeness()
            db.session.commit()
        except:
            abort(404, message="Somethig went wrong")

        response = make_response()
        response.status_code = 200
        return response


    def patch(self, gym_id):
        args = parser.parse_args()
        gym = abort_if_gym_doesnt_exist(gym_id)

        abort_if_etag_doesnt_match(args['If-None-Match'], gym.get_hash())

        if args['name'] is not None:
            gym.name = args['name']
        if args['location'] is not None:
            gym.location = args['location']
        try:
            gym.check_completeness()
            db.session.commit()
        except:
            abort(404, message="Somethig went wrong")

        response = make_response()
        response.status_code = 200
        return response

        
    def delete(self, gym_id):
        abort_if_gym_doesnt_exist(gym_id)

        try:
             GymModel.query.filter(GymModel.id == int(gym_id)).delete()
             db.session.commit()
             response = make_response()
             response.status_code = 204
             return response
        except: 
            abort(404, message="Somethig went wrong")
        


class GymList(Resource):
    def get(self):
 
        args = request.args
        pagination = False

        if 'limit' in args and 'offset' in args:
            abort_if_limit_or_offset_is_bad(args)
            pagination = True

            per_page = int(args['limit'])
            page = int(args['offset'])/int(args['limit'])+1
            paginate_result = GymModel.query.filter(GymModel.is_created.is_(True)).paginate(page, per_page, False)
            gyms = paginate_result.items
        else:
            gyms = GymModel.query.filter(GymModel.is_created.is_(True)).all()
     
        response = make_response(jsonify(gyms))
        response.status_code = 200

        if pagination:
            limit = int(args['limit'])
            offset = int(args['offset'])

            response.headers['next'] = url_for('gymlist')+f'?limit={limit}&offset={offset+limit if paginate_result.total>=offset+limit else offset}'
            response.headers['prev'] = url_for('gymlist')+f'?limit={limit}&offset={max(offset-limit,0)}'
            response.headers['results'] = paginate_result.total

        return response

    def post(self):
        #args = parser.parse_args() NO POE
        gym = GymModel() 

        try:
            db.session.add(gym)
            db.session.commit()
        except:
            abort(404, message="Somethig went wrong")

        res_body = {
            'URL': url_for('gym', gym_id=gym.id),
            'ETag':  gym.get_hash()
        }

        response = make_response(jsonify(res_body))
        response.status_code = 201

        return response



class GymCleanup(Resource):
    def post(self, gym_id):

        gym = abort_if_gym_doesnt_exist(gym_id)

        try:
            equipment_affiliations = EquipmentAffiliationModel.query.filter(EquipmentAffiliationModel.gym_id==int(gym_id)).all()
            for eq in equipment_affiliations:
                eq.related_equipment.is_clean = True
            db.session.commit()
        except:
            abort(404, message="Somethig went wrong")

        res_body = {
            'message': f'Gym {gym_id} has been cleaned',
        }

        response = make_response(jsonify(res_body))
        response.status_code = 200

        return response

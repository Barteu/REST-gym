import datetime as dt
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource, url_for
from gym_app.models import GymMembershipModel
from gym_app import db
from flask import jsonify, make_response
from gym_app.utils import abort_if_limit_or_offset_is_bad, abort_if_etag_doesnt_match

parser = reqparse.RequestParser()
parser.add_argument('entries')
parser.add_argument('user_id')
parser.add_argument('gym_id')
parser.add_argument('If-None-Match', location='headers')


def abort_if_gym_membership_doesnt_exist(gym_membership_id):
    gym_membership =  GymMembershipModel.query.filter(GymMembershipModel.id == int(gym_membership_id)).first()
    if gym_membership is None:
        abort(404, message="Gym Membership {} doesn't exist".format(gym_membership_id))
    else:
        return gym_membership


class GymMembership(Resource):
    def get(self, gym_membership_id):
       
        gym_membership = abort_if_gym_membership_doesnt_exist(gym_membership_id)

        response = make_response(jsonify(gym_membership))
        response.status_code = 200
        response.headers['ETag'] = gym_membership.get_hash()

        return response


    def put(self, gym_membership_id):
        args = parser.parse_args()
        gym_membership = abort_if_gym_membership_doesnt_exist(gym_membership_id)
      
        abort_if_etag_doesnt_match(args['If-None-Match'], gym_membership.get_hash())

        if args['entries'] is not None:
            gym_membership.entries = args['entries']
        if args['user_id'] is not None:
            gym_membership.user_id = args['user_id']
        if args['gym_id'] is not None:
            gym_membership.gym_id = args['gym_id']
        try:
            gym_membership.check_completeness()
            db.session.commit()
        except:
            abort(404, message="Somethig went wrong")

        response = make_response()
        response.status_code = 200
        return response


    def patch(self, gym_membership_id):
        args = parser.parse_args()
        gym_membership = abort_if_gym_membership_doesnt_exist(gym_membership_id)

        abort_if_etag_doesnt_match(args['If-None-Match'], gym_membership.get_hash())

        if args['entries'] is not None:
            gym_membership.entries = args['entries']
        if args['user_id'] is not None:
            gym_membership.user_id = args['user_id']
        if args['gym_id'] is not None:
            gym_membership.gym_id = args['gym_id']
        try:
            gym_membership.check_completeness()
            db.session.commit()
        except:
            abort(404, message="Somethig went wrong")

        response = make_response()
        response.status_code = 200
        return response

        
    def delete(self, gym_membership_id):
        abort_if_gym_membership_doesnt_exist(gym_membership_id)

        try:
             GymMembershipModel.query.filter(GymMembershipModel.id == int(gym_membership_id)).delete()
             db.session.commit()
             response = make_response()
             response.status_code = 204
             return response
        except: 
            abort(404, message="Somethig went wrong")
        

class GymMembershipList(Resource):
    def get(self):
 
        args = request.args
        pagination = False

        if 'limit' in args and 'offset' in args:
            abort_if_limit_or_offset_is_bad(args)
            pagination = True

            per_page = int(args['limit'])
            page = int(args['offset'])/int(args['limit'])+1
            paginate_result = GymMembershipModel.query.filter(GymMembershipModel.is_created.is_(True)).paginate(page, per_page, False)
            gym_memberships = paginate_result.items
        else:
            gym_memberships = GymMembershipModel.query.filter(GymMembershipModel.is_created.is_(True)).all()
     
        response = make_response(jsonify(gym_memberships))
        response.status_code = 200

        if pagination:
            limit = int(args['limit'])
            offset = int(args['offset'])

            response.headers['next'] = url_for('gymmembershiplist')+f'?limit={limit}&offset={offset+limit if paginate_result.total>=offset+limit else offset}'
            response.headers['prev'] = url_for('gymmembershiplist')+f'?limit={limit}&offset={max(offset-limit,0)}'
            response.headers['results'] = paginate_result.total
            
        return response

    def post(self):
       
        gym_membership = GymMembershipModel() 

        args = parser.parse_args()
        if args['entries'] is not None:
            gym_membership.entries = args['entries']
        if args['user_id'] is not None:
            gym_membership.user_id = args['user_id']
        if args['gym_id'] is not None:
            gym_membership.gym_id = args['gym_id']
        gym_membership.creation_date = dt.date.today()
        gym_membership.check_completeness()

        try:
            db.session.add(gym_membership)    
            db.session.commit()
        except:
            abort(404, message="Somethig went wrong")

        res_body = {
            'URL': url_for('gymmembership', gym_membership_id=gym_membership.id),
            'ETag':  gym_membership.get_hash()
        }

        response = make_response(jsonify(res_body))
        response.status_code = 201

        return response



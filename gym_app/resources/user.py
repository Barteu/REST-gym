from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource, url_for
from gym_app.models import UserModel
from gym_app import db
from flask import jsonify, make_response
from gym_app.utils import abort_if_limit_or_offset_is_bad, abort_if_etag_doesnt_match

parser = reqparse.RequestParser()
parser.add_argument('first_name')
parser.add_argument('last_name')
parser.add_argument('birth_year')
parser.add_argument('If-None-Match', location='headers')


def abort_if_user_doesnt_exist(user_id):
    user =  UserModel.query.filter(UserModel.id == int(user_id)).first()
    if user is None:
        abort(404, message="User {} doesn't exist".format(user_id))
    else:
        return user


class User(Resource):
    def get(self, user_id):
       
        user = abort_if_user_doesnt_exist(user_id)

        response = make_response(jsonify(user))
        response.status_code = 200
        response.headers['ETag'] = user.get_hash()

        return response


    def put(self, user_id):
        args = parser.parse_args()
        user = abort_if_user_doesnt_exist(user_id)
      
        abort_if_etag_doesnt_match(args['If-None-Match'], user.get_hash())

        try:
            if args['first_name'] is not None:
                user.first_name = args['first_name']
            if args['last_name'] is not None:
                user.last_name = args['last_name']
            if args['birth_year'] is not None:
                user.birth_year = int(args['birth_year'])
        except:
            abort(400, message="Bad data format")
        
        try:
            user.check_completeness()
            db.session.commit()
        except:
            abort(404, message="Somethig went wrong")

        response = make_response()
        response.status_code = 200
        return response


    def patch(self, user_id):
        args = parser.parse_args()
        user = abort_if_user_doesnt_exist(user_id)

        abort_if_etag_doesnt_match(args['If-None-Match'], user.get_hash())

        try:
            user.last_name = args['last_name']
        except:
            abort(400, message="Bad data format")           
   
        try:
            user.check_completeness()
            db.session.commit()
        except:
            abort(404, message="Somethig went wrong")

        response = make_response()
        response.status_code = 200
        return response

        
    def delete(self, user_id):
        abort_if_user_doesnt_exist(user_id)

        try:
             UserModel.query.filter(UserModel.id == int(user_id)).delete()
             db.session.commit()
             response = make_response()
             response.status_code = 204
             return response
        except: 
            abort(404, message="Somethig went wrong")
        

class UserList(Resource):
    def get(self):
 
        args = request.args
        pagination = False

        if 'limit' in args and 'offset' in args:
            abort_if_limit_or_offset_is_bad(args)
            pagination = True

            per_page = int(args['limit'])
            page = int(args['offset'])/int(args['limit'])+1
            paginate_result = UserModel.query.filter(UserModel.is_created.is_(True)).paginate(page, per_page, False)
            users = paginate_result.items
        else:
            users = UserModel.query.filter(UserModel.is_created.is_(True)).all()
     
        response = make_response(jsonify(users))
        response.status_code = 200

        if pagination:
            limit = int(args['limit'])
            offset = int(args['offset'])

            response.headers['next'] = url_for('userlist')+f'?limit={limit}&offset={offset+limit if paginate_result.total>=offset+limit else offset}'
            response.headers['prev'] = url_for('userlist')+f'?limit={limit}&offset={max(offset-limit,0)}'
            response.headers['results'] = paginate_result.total

        return response

    def post(self):
        #args = parser.parse_args() NO POE
        user = UserModel() 

        try:
            db.session.add(user)
            db.session.commit()
        except:
            abort(404, message="Somethig went wrong")

        res_body = {
            'URL': url_for('user', user_id=user.id),
            'ETag':  user.get_hash()
        }

        response = make_response(jsonify(res_body))
        response.status_code = 201

        return response


from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource, url_for
from gym_app.models import EquipmentAffiliationModel, GymModel, EquipmentModel
from gym_app import db
from flask import jsonify, make_response
from gym_app.resources.gym import Gym
from gym_app.utils import abort_if_limit_or_offset_is_bad, abort_if_etag_doesnt_match

parser = reqparse.RequestParser()
parser.add_argument('equipment_id', type=int)
parser.add_argument('gym_id', type=int)
parser.add_argument('If-None-Match', location='headers')


def abort_if_equipment_affiliation_doesnt_exist(id):
    equipment_affiliation =  EquipmentAffiliationModel.query.filter(EquipmentAffiliationModel.id == int(id)).first()
    if equipment_affiliation is None:
        abort(404, message="Equipment Affiliation {} doesn't exist".format(id))
    else:
        return equipment_affiliation


class EquipmentAffiliation(Resource):
    def get(self, id):
       
        equipment_affiliation = abort_if_equipment_affiliation_doesnt_exist(id)

        response = make_response(jsonify(equipment_affiliation))
        response.status_code = 200
        response.headers['ETag'] = equipment_affiliation.get_hash()

        return response


    def put(self, id):
        args = parser.parse_args()
        equipment_affiliation = abort_if_equipment_affiliation_doesnt_exist(id)
      
        abort_if_etag_doesnt_match(args['If-None-Match'], equipment_affiliation.get_hash())

        try:
            if args['equipment_id'] is not None:
                if EquipmentModel.query.filter(EquipmentModel.id == int(args['equipment_id'])).first() is None:
                    raise Exception()
                equipment_affiliation.equipment_id = args['equipment_id']
            if args['gym_id'] is not None:
                if GymModel.query.filter(GymModel.id == int(args['gym_id'])).first() is None:
                    raise Exception()
                equipment_affiliation.gym_id = args['gym_id']
        except:
            abort(400, message="Bad data format")
       
        try:
            equipment_affiliation.check_completeness()
            db.session.commit()
        except:
            abort(404, message="Somethig went wrong")

        response = make_response()
        response.status_code = 200
        return response


    def patch(self, id):
        args = parser.parse_args()
        equipment_affiliation = abort_if_equipment_affiliation_doesnt_exist(id)

        abort_if_etag_doesnt_match(args['If-None-Match'], equipment_affiliation.get_hash())

        try:
            if args['equipment_id'] is not None:
                equipment_affiliation.equipment_id = args['equipment_id']
            if args['gym_id'] is not None:
                equipment_affiliation.gym_id = args['gym_id']
        except:
            abort(400, message="Bad data format")
        try:
            equipment_affiliation.check_completeness()
            db.session.commit()
        except:
            abort(404, message="Somethig went wrong")

        response = make_response()
        response.status_code = 200
        return response

        
    def delete(self, id):
        abort_if_equipment_affiliation_doesnt_exist(id)

        try:
             EquipmentAffiliationModel.query.filter(EquipmentAffiliationModel.id == int(id)).delete()
             db.session.commit()
             response = make_response()
             response.status_code = 204
             return response
        except: 
            abort(404, message="Somethig went wrong")
        

class EquipmentAffiliationList(Resource):
    def get(self):
 
        args = request.args
        pagination = False

        if 'limit' in args and 'offset' in args:
            abort_if_limit_or_offset_is_bad(args)
            pagination = True

            per_page = int(args['limit'])
            page = int(args['offset'])/int(args['limit'])+1
            paginate_result = EquipmentAffiliationModel.query.filter(EquipmentAffiliationModel.is_created.is_(True)).paginate(page, per_page, False)
            equipment_affiliations = paginate_result.items
        else:
            equipment_affiliations = EquipmentAffiliationModel.query.filter(EquipmentAffiliationModel.is_created.is_(True)).all()
     
        response = make_response(jsonify(equipment_affiliations))
        response.status_code = 200

        if pagination:
            limit = int(args['limit'])
            offset = int(args['offset'])

            response.headers['next'] = url_for('equipmentaffiliationlist')+f'?limit={limit}&offset={offset+limit if paginate_result.total>=offset+limit else offset}'
            response.headers['prev'] = url_for('equipmentaffiliationlist')+f'?limit={limit}&offset={max(offset-limit,0)}'
            response.headers['results'] = paginate_result.total
            
        return response

    def post(self):
        #args = parser.parse_args() NO POE
        equipment_affiliation = EquipmentAffiliationModel() 

        try:
            db.session.add(equipment_affiliation)
            db.session.commit()
        except:
            abort(404, message="Somethig went wrong")

        res_body = {
            'URL': url_for('equipmentaffiliation', id=equipment_affiliation.id),
            'ETag':  equipment_affiliation.get_hash()
        }

        response = make_response(jsonify(res_body))
        response.status_code = 201

        return response


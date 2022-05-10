from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource, url_for
from gym_app.models import EquipmentModel
from gym_app import db
from flask import jsonify, make_response
from gym_app.utils import abort_if_limit_or_offset_is_bad, abort_if_etag_doesnt_match

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('is_clean')
parser.add_argument('If-None-Match', location='headers')


def abort_if_equipment_doesnt_exist(equipment_id):
    equipment =  EquipmentModel.query.filter(EquipmentModel.id == int(equipment_id)).first()
    if equipment is None:
        abort(404, message="Equipment {} doesn't exist".format(equipment_id))
    else:
        return equipment


class Equipment(Resource):
    def get(self, equipment_id):
       
        equipment = abort_if_equipment_doesnt_exist(equipment_id)

        response = make_response(jsonify(equipment))
        response.status_code = 200
        response.headers['ETag'] = equipment.get_hash()

        return response


    def put(self, equipment_id):
        args = parser.parse_args()
        equipment = abort_if_equipment_doesnt_exist(equipment_id)
      
        abort_if_etag_doesnt_match(args['If-None-Match'], equipment.get_hash())

        if args['name'] is not None:
            equipment.name = args['name']
        if args['is_clean'] is not None:
            equipment.is_clean = args['is_clean']
        try:
            equipment.check_completeness()
            db.session.commit()
        except:
            abort(404, message="Somethig went wrong")

        response = make_response()
        response.status_code = 200
        return response


    def patch(self, equipment_id):
        args = parser.parse_args()
        equipment = abort_if_equipment_doesnt_exist(equipment_id)

        abort_if_etag_doesnt_match(args['If-None-Match'], equipment.get_hash())

        if args['name'] is not None:
            equipment.name = args['name']
        if args['is_clean'] is not None:
            equipment.is_clean = args['is_clean']
        try:
            equipment.check_completeness()
            db.session.commit()
        except:
            abort(404, message="Somethig went wrong")

        response = make_response()
        response.status_code = 200
        return response

        
    def delete(self, equipment_id):
        abort_if_equipment_doesnt_exist(equipment_id)

        try:
             EquipmentModel.query.filter(EquipmentModel.id == int(equipment_id)).delete()
             db.session.commit()
             response = make_response()
             response.status_code = 204
             return response
        except: 
            abort(404, message="Somethig went wrong")
        

class EquipmentList(Resource):
    def get(self):
 
        args = request.args
        pagination = False

        if 'limit' in args and 'offset' in args:
            abort_if_limit_or_offset_is_bad(args)
            pagination = True

            per_page = int(args['limit'])
            page = int(args['offset'])/int(args['limit'])+1
            paginate_result = EquipmentModel.query.filter(EquipmentModel.is_created.is_(True)).paginate(page, per_page, False)
            equipments = paginate_result.items
        else:
            equipments = EquipmentModel.query.filter(EquipmentModel.is_created.is_(True)).all()
     
        response = make_response(jsonify(equipments))
        response.status_code = 200

        if pagination:
            limit = int(args['limit'])
            offset = int(args['offset'])

            response.headers['next'] = url_for('equipmentlist')+f'?limit={limit}&offset={offset+limit if paginate_result.total>=offset+limit else offset}'
            response.headers['prev'] = url_for('equipmentlist')+f'?limit={limit}&offset={max(offset-limit,0)}'
            response.headers['results'] = paginate_result.total
            
        return response

    def post(self):
       
        equipment = EquipmentModel() 

        try:
            db.session.add(equipment)
            db.session.commit()
        except:
            abort(404, message="Somethig went wrong")

        res_body = {
            'URL': url_for('equipment', equipment_id=equipment.id),
            'ETag':  equipment.get_hash()
        }

        response = make_response(jsonify(res_body))
        response.status_code = 201

        return response


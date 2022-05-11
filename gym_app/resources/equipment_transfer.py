from email import message
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource, url_for
from gym_app.models import EquipmentModel, EquipmentAffiliationModel, GymModel
from gym_app import db
from flask import jsonify, make_response
from gym_app.utils import abort_if_etag_doesnt_match



def abort_if_equipment_doesnt_exist(equipment_id):
    equipment =  EquipmentModel.query.filter(EquipmentModel.id == int(equipment_id)).first()
    if equipment is None:
        abort(404, message="Equipment {} doesn't exist".format(equipment_id))
    else:
        return equipment


class EquipmentTransfer(Resource):
    def post(self):
        if(request.data):
    
            jdata = request.get_json()
    
            db.session.begin()
            try:
                for transfer in jdata['transfers']:
                    eq_id = int(transfer['equipment_id'])
                    gym_id = int(transfer['new_gym_id'])
                    if GymModel.query.filter(GymModel.id==gym_id).first() is not None and\
                        EquipmentModel.query.filter(EquipmentModel.id==eq_id).first() is not None:
                        eq_affil = EquipmentAffiliationModel.query.filter(EquipmentAffiliationModel.equipment_id==eq_id).first()
                        eq_affil.gym_id = gym_id
                    else:
                        raise Exception("Bad gym or equipment id")
                db.session.commit()
            except:
                db.session.rollback()
                abort(400, message="Error in JSON data")
        else:
            abort(400, message="No data found")

        response = make_response()
        response.status_code = 200

        return response


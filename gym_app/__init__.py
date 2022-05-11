from flask import Flask
from flask_restful import Api

from gym_app.extensions import db

from gym_app.resources.gym import Gym, GymList, GymCleanup
from gym_app.resources.gym_membership import GymMembership, GymMembershipList
from gym_app.resources.user import User, UserList
from gym_app.resources.equipment import Equipment, EquipmentList
from gym_app.resources.equipment_affiliation import EquipmentAffiliation, EquipmentAffiliationList
from gym_app.resources.equipment_transfer import EquipmentTransfer

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

api.add_resource(GymList, '/gyms')
api.add_resource(Gym, '/gyms/<gym_id>')
api.add_resource(GymCleanup, '/gyms/<gym_id>/cleanups')

api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<user_id>')

api.add_resource(GymMembershipList, '/gym-memberships')
api.add_resource(GymMembership, '/gym-memberships/<gym_membership_id>')

api.add_resource(EquipmentList, '/equipments')
api.add_resource(Equipment, '/equipments/<equipment_id>')

api.add_resource(EquipmentAffiliationList, '/equipment-affiliations')
api.add_resource(EquipmentAffiliation, '/equipment-affiliations/<id>')

api.add_resource(EquipmentTransfer, '/equipment-transfers')


from gym_app import models

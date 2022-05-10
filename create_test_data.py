from ctypes import memmove
from operator import eq
from gym_app import db
from gym_app.models import *
import datetime as dt

gym1 = GymModel()
gym1.name = "PudzianPro"
gym1.location = "Kornicka 92, Poznan"
gym1.is_created = True
db.session.add(gym1)

gym2 = GymModel()
gym2.name = "FitnessPro"
gym2.location = "Niepodleglosci 8, Poznan"
gym2.is_created = True
db.session.add(gym2)


user1 = UserModel()
user1.first_name = "Jack"
user1.last_name = "Kowalsky"
user1.birth_year = 1982
user1.is_created = True
db.session.add(user1)

user2 = UserModel()
user2.first_name = "John"
user2.last_name = "Doe"
user2.birth_year = 1970
user2.is_created = True
db.session.add(user2)


db.session.flush()


membership1= GymMembershipModel()
membership1.entries = 10
membership1.gym_id = gym1.id
membership1.user_id = user1.id
membership1.creation_date = dt.date.today()
membership1.is_created = True
db.session.add(membership1)

for i in range(20):
    equipment = EquipmentModel()
    equipment.name = f"dumbbells{i}"
    equipment.is_clean = True if i%2==0 else False
    equipment.is_created = True
    db.session.add(equipment)
    db.session.flush()
    
    eqa = EquipmentAffiliationModel()
    eqa.gym_id = gym1.id if i%2==0 else gym2.id
    eqa.equipment_id = equipment.id
    eqa.is_created = True
    db.session.add(eqa)

equipment1 = EquipmentModel()
equipment1.name = "barbells"
equipment1.is_clean = True
equipment1.is_created = True
db.session.add(equipment1)



db.session.commit()

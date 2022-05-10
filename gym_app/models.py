from email.policy import default
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from gym_app import db

from dataclasses import dataclass
from gym_app.extensions import  hash_tup
import datetime as dt


@dataclass
class GymModel(db.Model):
    __tablename__ = "gyms"
    
    id: int
    name: str
    location: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=True)
    location = db.Column(db.String(128), unique=False, nullable=True)

    # POE
    is_created =  db.Column(db.Boolean, default=False) 

    def __repr__(self):
        return f'<Gym {self.id} {self.name}>'

    def get_hash(self):
        return hash_tup((self.id, self.name, self.location))

    def check_completeness(self):
        if self.name != None and self.location != None:
            self.is_created = True
            return True
        else:
            return False


@dataclass
class UserModel(db.Model):
    __tablename__ = "users"

    id: int
    first_name: str
    last_name: str
    birth_year: int

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), unique=False, nullable=True)
    last_name = db.Column(db.String(100), unique=False, nullable=True)
    birth_year = db.Column(db.Integer, nullable=True)

    # POE
    is_created =  db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User: {self.id} {self.first_name} {self.last_name}>'

    def get_hash(self):
        return hash_tup((self.id, self.first_name, self.last_name, self.birth_year))

    def check_completeness(self):
        if self.first_name != None\
             and self.last_name != None\
                and self.birth_year != None:
            self.is_created = True
            return True
        else:
            return False


@dataclass
class GymMembershipModel(db.Model):
    __tablename__ = "gym_memberships"

    id: int
    entries: int
    gym_id: int
    user_id: int
    creation_date: dt.date

    id = db.Column(db.Integer, primary_key=True)
    entries = db.Column(db.Integer, default=0)
    creation_date = db.Column(db.Date, nullable=True)

    gym_id = db.Column(db.Integer, db.ForeignKey('gyms.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # POE
    is_created =  db.Column(db.Boolean, default=False)

    def __repr__(self):
          return f'<GymMembership: {self.id}>'

    def get_hash(self):
        return hash_tup((self.id, self.entries, self.gym_id, self.user_id, self.creation_date))

    def check_completeness(self):
        if self.gym_id != None\
             and self.user_id != None\
                and self.entries != None:
            self.is_created = True
            return True
        else:
            return False


@dataclass
class EquipmentModel(db.Model):
    __tablename__ = "equipments"

    id: int
    name: int
    is_clean: bool

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    is_clean = db.Column(db.Boolean, default=True)

 
    # POE
    is_created =  db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Equipment: {self.id} {self.name} clean: {self.is_clean}>'

    def get_hash(self):
        return hash_tup((self.id, self.name, self.is_clean, self.gym))

    def check_completeness(self):
        if self.name != None\
             and self.gym != None:
            self.is_created = True
            return True
        else:
            return False


@dataclass
class EquipmentAffiliationModel(db.Model):
    __tablename__ = "equipment_affiliations"

    id: int
    equipment_id: int
    gym_id: int

    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'), nullable=True)
    gym_id = db.Column(db.Integer, db.ForeignKey('gyms.id'), nullable=True)

    related_equipment = relationship("EquipmentModel", foreign_keys=[equipment_id])

    # POE
    is_created =  db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Equipment: {self.id} {self.equipment_id} {self.gym_id}>'

    def get_hash(self):
        return hash_tup((self.id, self.equipment_id, self.gym_id))

    def check_completeness(self):
        if self.equipment_id != None\
             and self.gym_id != None:
            self.is_created = True
            return True
        else:
            return False
from email.policy import default
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from gym_app import db

from dataclasses import dataclass


@dataclass
class GymModel(db.Model):
    __tablename__ = "gyms"
    
    id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)

    def __repr__(self):
        return f'<Gym {self.id} {self.name}>'

    def __hash__(self):
        return hash((self.id, self.name))

    

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), unique=False, nullable=False)
    last_name = db.Column(db.String(100), unique=False, nullable=False)

    def __repr__(self):
        return f'<User: {self.id} {self.first_name} {self.last_name}>'

    def __hash__(self):
        return hash((self.id, self.first_name, self.last_name))



class GymMembershipModel(db.Model):
    __tablename__ = "gym_memberships"
    id = db.Column(db.Integer, primary_key=True)
    entries = db.Column(db.Integer, default=0)

    gym = db.Column(db.Integer, db.ForeignKey('gyms.id'))
    user = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
          return f'<GymMembership: {self.id}>'

    def __hash__(self):
        return hash((self.id, self.entries, self.gym, self.user))



class Equipment(db.Model):
    __tablename__ = "equipments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, primary_key=True)
    is_clean = db.Column(db.Boolean, default=True)

    gym = db.Column(db.Integer, db.ForeignKey('gyms.id'))

    def __repr__(self):
        return f'<Equipment: {self.id} {self.name} clean: {self.is_clean}>'

    def __hash__(self):
        return hash((self.id, self.name, self.is_clean, self.gym))

  

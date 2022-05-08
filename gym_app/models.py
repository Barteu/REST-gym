from email.policy import default
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from gym_app import db

from dataclasses import dataclass
from gym_app.extensions import  hash_tup


@dataclass
class GymModel(db.Model):
    __tablename__ = "gyms"
    
    id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)

    def __repr__(self):
        return f'<Gym {self.id} {self.name}>'

    def get_hash(self):
        return hash_tup((self.id, self.name))


@dataclass
class UserModel(db.Model):
    __tablename__ = "users"

    id: int
    first_name: str
    last_name: str

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), unique=False, nullable=False)
    last_name = db.Column(db.String(100), unique=False, nullable=False)

    def __repr__(self):
        return f'<User: {self.id} {self.first_name} {self.last_name}>'

    def get_hash(self):
        return hash_tup((self.id, self.first_name, self.last_name))


@dataclass
class GymMembershipModel(db.Model):
    __tablename__ = "gym_memberships"

    id: int
    entries: int
    gym: int
    user: int

    id = db.Column(db.Integer, primary_key=True)
    entries = db.Column(db.Integer, default=0)

    gym = db.Column(db.Integer, db.ForeignKey('gyms.id'))
    user = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
          return f'<GymMembership: {self.id}>'

    def get_hash(self):
        return hash_tup((self.id, self.entries, self.gym, self.user))


@dataclass
class Equipment(db.Model):
    __tablename__ = "equipments"

    id: int
    name: int
    is_clean: bool
    gym: int

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), primary_key=True)
    is_clean = db.Column(db.Boolean, default=True)

    gym = db.Column(db.Integer, db.ForeignKey('gyms.id'))


    def __repr__(self):
        return f'<Equipment: {self.id} {self.name} clean: {self.is_clean}>'

    def get_hash(self):
        return hash_tup((self.id, self.name, self.is_clean, self.gym))

  

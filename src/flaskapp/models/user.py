import sys
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from flask import jsonify
sys.path.append('..')
from database import Base, db_session
from models.user_stats import User_stats
from models.champions_played import Champions_played
from models.roles_played import Roles_played

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    email = Column(String(120), unique=False)
    password = Column(String(120), unique=False)
    riot_id = Column(String(120), unique=False)
    puuid = Column(String(120), unique=False)

    user_stats = relationship('User_stats', back_populates = 'user_object', uselist=False)
    champions_played = relationship('Champions_played', back_populates = 'user_object')
    roles_played = relationship('Roles_played', back_populates = 'user_object')
    tournament_stats = relationship('Tournament_stats', back_populates = 'user_object')

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def save(self):
        db_session.add(self)
        db_session.commit()

    def __repr__(self):
        return f'<User {self.username!r}>'
    
    def json(self):
        return jsonify({'id': self.id, 'username': self.username, 'email': self.email, 'riot_id': self.riot_id, 'puuid': self.puuid})
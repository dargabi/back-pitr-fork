import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped
from flask import jsonify

sys.path.append('..')
from database import Base, db_session

class Roles_played(Base):
    __tablename__ = 'roles_played'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    role = Column(String(10))
    games = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    kills = Column(Integer)
    deaths = Column(Integer)
    assists = Column(Integer)

    user_object = relationship('User', back_populates = 'roles_played')


    def __init__(self, user_id=0, role=None, games=0, wins=0, losses=0, kills=0, deaths=0, assists=0):
        self.user_id = user_id
        self.role = role
        self.games = games
        self.wins = wins
        self.losses = losses
        self.kills = kills
        self.deaths = deaths
        self.assists = assists

    def save(self):
        db_session.add(self)
        db_session.commit()

    def __repr__(self):
        return f'<{self.user_id!r} {self.role!r}>'
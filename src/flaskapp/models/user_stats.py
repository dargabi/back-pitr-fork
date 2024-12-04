import sys
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped
from flask import jsonify

sys.path.append('..')
from database import Base, db_session

class User_stats(Base):
    __tablename__ = 'users_stats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    wins = Column(Integer)
    losses = Column(Integer)
    kills = Column(Integer)
    deaths = Column(Integer)
    assists = Column(Integer)
    mmr = Column(Integer)
    score = Column(Integer)
    rank = Column(Integer)

    user_object = relationship('User', back_populates = 'user_stats')

    def __init__(self, user_id=0, wins=0, losses=0, kills=0, deaths=0, assists=0, mmr=0, score = 0, rank=99999):
        self.user_id = user_id
        self.wins = wins
        self.losses = losses
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.mmr = mmr
        self.score = score
        self.rank = rank
    
    def save(self):
        db_session.add(self)
        db_session.commit()
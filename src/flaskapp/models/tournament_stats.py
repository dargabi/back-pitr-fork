import sys
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from flask import jsonify
sys.path.append('..')
from database import Base, db_session

class Tournament_stats(Base):
    __tablename__ = 'tournament_stats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    wins = Column(Integer, unique=False)
    losses = Column(Integer, unique=False)
    score = Column(Integer, unique=False)
    rank = Column(Integer, unique=False)

    tournament_object = relationship('Tournament', back_populates = 'tournament_stats')
    user_object = relationship('User', back_populates = 'tournament_stats')

    def __init__(self, tournament_id=None, user_id=None, wins=0, losses=0, score=0, rank=99999):
        self.tournament_id = tournament_id
        self.user_id = user_id
        self.wins = wins
        self.losses = losses
        self.score = score
        self.rank = rank
    
    def save(self):
        db_session.add(self)
        db_session.commit()
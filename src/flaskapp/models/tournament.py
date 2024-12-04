import sys
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
import datetime

sys.path.append('..')
from database import Base, db_session

class Tournament(Base):
    __tablename__ = 'tournaments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(Date, unique=False)
    end_date = Column(Date, unique=False)
    name = Column(String(50), unique=False)
    description = Column(String(200), unique=False)
    server = Column(String(10), unique=False)
    team_size = Column(Integer, unique=False)

    tournament_stats = relationship('Tournament_stats', back_populates = 'tournament_object')

    def __init__(self, start_date=None, end_date=None, name=None, description=None, server=None, team_size=None):
        self.start_date = start_date
        self.end_date = end_date
        self.name = name
        self.description = description
        self.server = server
        self.team_size = team_size

    def save(self):
        db_session.add(self)
        db_session.commit()

    def is_active(self):
        start_str = str(self.start_date)
        end_str = str(self.end_date)
        now_str = str(datetime.datetime.now().date())

        return start_str <= now_str and now_str <= end_str
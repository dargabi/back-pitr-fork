import os
from sqlalchemy  import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from flask import current_app
from env_secrets import secrets

# Create the database engine
engine = create_engine(secrets['DATABASE_URI'])

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()

    from models.user import User
    # Create the database tables or update them if they exist
    Base.metadata.create_all(bind=engine)
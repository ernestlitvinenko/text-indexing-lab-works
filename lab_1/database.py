from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

engine = create_engine('sqlite:///database.db')
session_maker = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


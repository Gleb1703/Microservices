from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query'

engine = create_engine(URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class MovieDB(Base):
    __tablename__ = 'movie_klyukoyt'

    id = Column(Integer, primary_key=True)
    movie_name = Column(String, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    genre = Column(String, nullable=False)
    director = Column(String, nullable=False)

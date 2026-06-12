from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///f1.db", echo=False)

Base = declarative_base()

class RaceResult(Base):
    __tablename__ = "race_results"

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    race = Column(String)
    position = Column(Integer)
    driver = Column(String)
    team = Column(String)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

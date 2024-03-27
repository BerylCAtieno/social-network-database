from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

#database parameters
username = 'social_2'
password = 'password'
hostname = 'localhost'
port = '5432'  
database_name = 'social_network_db'

# Create the engine URL
database_url = f"postgresql://{username}:{password}@{hostname}:{port}/{database_name}"

engine = create_engine(database_url)
Base = declarative_base()


class Place(Base):
    __tablename__ = 'place'
    placeID = Column(Integer, primary_key=True)
    name = Column(String(255))

class Continent(Place):
    __tablename__ = 'continent'
    continentID = Column(Integer, ForeignKey('place.placeID'), primary_key=True)

class Country(Place):
    __tablename__ = 'country'
    countryID = Column(Integer, primary_key=True)
    continentID = Column(Integer, ForeignKey('continent.continentID'))
    continent = relationship("Continent")

class City(Place):
    __tablename__ = 'city'
    cityID = Column(Integer, primary_key=True)
    countryID = Column(Integer, ForeignKey('country.countryID'))
    country = relationship("Country")

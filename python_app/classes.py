from sqlalchemy import Table
from create_engine import engine
#from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base



"""class Base(DeclarativeBase):
    pass"""
Base = declarative_base()

Base.metadata.reflect(engine, views=True)
session = scoped_session(sessionmaker(bind=engine))


class Place(Base):
    __table__ = Table('place', Base.metadata, autoload_with=engine)
    
    __mapper_args__ = {
        'polymorphic_identity': 'place',
        'polymorphic_on': 'placeID'
    }
    

class Continent(Place):
    
    __mapper_args__ = {
        "polymorphic_identity": "continent",
    }

class Country(Place):

    __mapper_args__ = {
        "polymorphic_identity": "country",
    }

class City(Place):

    __mapper_args__ = {
        "polymorphic_identity": "city",
    }

class Person(Base):

    __table__ = Table('person', Base.metadata, autoload_with=engine)
    

class PersonEmail(Base):
   __table__ = Table('personemail', Base.metadata, autoload_with=engine)

class Language(Base):
    __table__ = Table('language', Base.metadata, autoload_with=engine)
    

class Forum(Base):
    __table__ = Table('forum', Base.metadata, autoload_with=engine)
    

class Message(Base):
    __table__ = Table('message', Base.metadata, autoload_with=engine)
    
    __mapper_args__ = {
        'polymorphic_identity': 'message',
        'polymorphic_on': 'messageID'
    }

class Post(Message):
   
    __mapper_args__ = {
        'polymorphic_identity': 'post'
    }

class Comment(Base):
    __table__ = Table('comment', Base.metadata, autoload_with=engine)

class tag(Base):
    __table__ = Table('tag', Base.metadata, autoload_with=engine)

    
class tagClass(Base):
    __table__ = Table('tagclass', Base.metadata, autoload_with=engine)



class tagClass_isSubclassof(Base):
    __table__ = Table('tagClass_isSubclassof', Base.metadata, autoload_with=engine)

  
class Message_hasTag(Base):
    __table__ = Table('message_hasTag', Base.metadata, autoload_with=engine)
    

class Forum_hasTag(Base):
    __table__ = Table('forum_hasTag', Base.metadata, autoload_with=engine)
    

class Forum_hasMember(Base):
    __table__ = Table('forum_hasMember', Base.metadata, autoload_with=engine)


class Person_likes_Message(Base):
     __table__ = Table('person_likes_Message', Base.metadata, autoload_with=engine)


class Person_likes_Comment(Base):
    __table__ = Table('person_likes_Comment', Base.metadata, autoload_with=engine)


class Person_knows_Person(Base):
    __table__ = Table('person_knows_person', Base.metadata, autoload_with=engine)


class Person_hasinterest(Base):
    __table__ = Table('person_has_interest', Base.metadata, autoload_with=engine)


class Organisation(Base):
    __tablename__ = 'organisation'

    __mapper_args__ = {
        'polymorphic_identity': 'organisation',
        'polymorphic_on': 'organisationID'
    }

class Company(Organisation):

    __mapper_args__ = {
        "polymorphic_identity": "company",
    }

class University(Organisation):
    
    __mapper_args__ = {
        "polymorphic_identity": "university",
    }

class StudyAt(Base):
    __table__ = Table('studyAt', Base.metadata, autoload_with=engine)


class WorkAt(Base):
    __table__ = Table('workAt', Base.metadata, autoload_with=engine)

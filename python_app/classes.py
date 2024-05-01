from sqlalchemy import Table
from create_engine import engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
Base.metadata.reflect(engine, views=True)
session = scoped_session(sessionmaker(bind=engine))


class Place(Base):
    __table__ = Table('place', Base.metadata, autoload_with=engine)
    
    __mapper_args__ = {
        'polymorphic_identity': 'place',
        'polymorphic_on': 'type'
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
""
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
    

class Post(Base):
    __table__ = Table('post', Base.metadata, autoload_with=engine)

class Comment(Base):
    __table__ = Table('comment', Base.metadata, autoload_with=engine)

class tag(Base):
    __table__ = Table('tag', Base.metadata, autoload_with=engine)

    
class tagClass(Base):
    __table__ = Table('tagclass', Base.metadata, autoload_with=engine)



class tagClass_isSubclassof(Base):
    __table__ = Table('tagclass_issubclassof', Base.metadata, autoload_with=engine)

  
class Message_hasTag(Base):
    __table__ = Table('message_hastag', Base.metadata, autoload_with=engine)
    

class Forum_hasTag(Base):
    __table__ = Table('forum_hastag', Base.metadata, autoload_with=engine)
    

class Forum_hasMember(Base):
    __table__ = Table('forum_hasmember', Base.metadata, autoload_with=engine)


class Person_likes_Message(Base):
     __table__ = Table('person_likes_message', Base.metadata, autoload_with=engine)


class Person_likes_Comment(Base):
    __table__ = Table('person_likes_comment', Base.metadata, autoload_with=engine)


class Person_knows_Person(Base):
    __table__ = Table('person_knows_person', Base.metadata, autoload_with=engine)


class Person_hasinterest(Base):
    __table__ = Table('person_hasinterest', Base.metadata, autoload_with=engine)


class Organisation(Base):
    __tablename__ = 'organisation'

    __mapper_args__ = {
        'polymorphic_identity': 'organisation',
        'polymorphic_on': 'type'
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
    __table__ = Table('studyat', Base.metadata, autoload=True, autoload_with=engine)


class WorkAt(Base):
    __table__ = Table('workat', Base.metadata, autoload=True, autoload_with=engine)
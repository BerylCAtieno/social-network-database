from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, BigInteger, SmallInteger, Date, TIMESTAMP
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint

import datetime
from typing import List 


class Base(DeclarativeBase):
    pass

class Place(Base):
    __tablename__ = 'place'
    
    placeID:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(55), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'place',
        'polymorphic_on': placeID
    }
    

class Continent(Place):
    __tablename__ = 'continent'
    
    continentID:Mapped[int] = mapped_column(ForeignKey('place.placeID'), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "continent",
    }
    
    extend_existing=True

class Country(Place):
    __tablename__ = 'country'
    
    countryID:Mapped[int] = mapped_column(ForeignKey('place.placeID'), primary_key=True)
    isPartOf:Mapped[int] = mapped_column(ForeignKey('continent.continentID'))

    __mapper_args__ = {
        "polymorphic_identity": "country",
    }

    extend_existing=True

    continent = relationship("Continent")

class City(Place):
    __tablename__ = 'city'
    
    cityID:Mapped[int] = mapped_column(ForeignKey('place.placeID'), primary_key=True)
    isPartOf:Mapped[int] = mapped_column(ForeignKey('country.countryID'))

    __mapper_args__ = {
        "polymorphic_identity": "city",
    }

    extend_existing=True

    country = relationship("Country")

class Person(Base):
    __tablename__ = 'person'
    
    personID:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    firstName:Mapped[str] = mapped_column(String(25), nullable=False)
    lastName :Mapped[str]= mapped_column(String(25), nullable=False)
    gender:Mapped[str] = mapped_column(String(25))
    birthday:Mapped[datetime.date] = mapped_column(nullable=False)
    creationDate = mapped_column(TIMESTAMP)
    locationIP:Mapped[str] = mapped_column(String(255))
    browserUsed:Mapped[str] = mapped_column(String(255))
    cityID:Mapped[int] = mapped_column(Integer, ForeignKey('city.cityID'))
    
    city = relationship("City")

    emails = relationship("PersonEmail", back_populates="person")
    languages = relationship("Language", back_populates="person")
    forums = relationship("Forum", back_populates="moderator")
    messages = relationship("Message", back_populates="creator")
    likes_messages = relationship("Person_likes_Message", back_populates="person")
    likes_comments = relationship("Person_likes_Comment", back_populates="person")
    knows_people = relationship("Person_knows_Person", back_populates="person")
    interests = relationship("Person_hasinterest", back_populates="person")

class PersonEmail(Base):
    __tablename__ = 'personemail'
    
    personID:Mapped[int] = mapped_column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    email:Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    person = relationship("Person", back_populates="emails")

class Language(Base):
    __tablename__ = 'language'
    
    personID:Mapped[int] = mapped_column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    language:Mapped[str] = mapped_column(String(255), nullable=False)

    person = relationship("Person", back_populates="languages")

class Forum(Base):
    __tablename__ = 'forum'
    
    forumID:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title:Mapped[str] = mapped_column(String(55))
    creationDate:Mapped[datetime.datetime] = mapped_column(TIMESTAMP)
    moderatorID:Mapped[int] = mapped_column(BigInteger, ForeignKey('person.personID'))

    moderator = relationship("Person", back_populates="forums")

class Message(Base):
    __tablename__ = 'message'
    
    messageID:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    content = mapped_column(String(255))
    length:Mapped[int] = mapped_column(Integer)
    creator:Mapped[int] = mapped_column(BigInteger, ForeignKey('person.personID'))
    countryID:Mapped[int] = mapped_column(BigInteger, ForeignKey('country.countryID'))
    creationDate:Mapped[datetime.datetime] = mapped_column(TIMESTAMP)
    browserused:Mapped[str] = mapped_column(String(55))
    locationIP:Mapped[str] = mapped_column(String(55))

    __mapper_args__ = {
        'polymorphic_identity': 'message',
        'polymorphic_on': messageID
    }

    creator = relationship("Person", back_populates="messages")

class Post(Message):
    __tablename__ = 'post'

    postID:Mapped[int] = mapped_column(BigInteger, ForeignKey('message.messageID'), primary_key=True)
    imageFile:Mapped[str] = mapped_column(String(255))
    forumID:Mapped[int] = mapped_column(BigInteger, ForeignKey('forum.forumID'))

    __mapper_args__ = {
        'polymorphic_identity': 'post'
    }

class Comment(Base):
    __tablename__ = 'comment'

    commentID:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    creationDate:Mapped[datetime.datetime] = mapped_column(TIMESTAMP)
    locationIP:Mapped[str] = mapped_column(String(50))
    browserUsed:Mapped[str] = mapped_column(String(50))
    content:Mapped[str] = mapped_column(String(255))
    length:Mapped[int] = mapped_column(Integer)
    creator:Mapped[int] = mapped_column(BigInteger)
    replyOfPost:Mapped[str] = mapped_column(String(50))
    replyOfComment:Mapped[str] = mapped_column(String(50))

class tag(Base):
    __tablename__ = 'tag'

    tagID:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name:Mapped[str] = mapped_column(String(255), nullable=False)
    url:Mapped[str] = mapped_column(String(2048))

class tagClass(Base):
    __tablename__ = 'tagclass'

    tagClassID:Mapped[int]= mapped_column(Integer, primary_key=True)
    tagClassName:Mapped[str] = mapped_column(String(255))
    url:Mapped[str] = mapped_column(String(2048))


class tagClass_isSubclassof(Base):
    __tablename__ = 'tagClass_isSubclassof'

    TagClassID_A:Mapped[int] = mapped_column(Integer)
    TagClassID_B:Mapped[int] = mapped_column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint(TagClassID_A, TagClassID_B),
        ForeignKeyConstraint(
            [TagClassID_A],
            ['tagClass.tagClassID'],
            onupdate="CASCADE",
            ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            [TagClassID_B],
            ['tag.tagID'],
            onupdate="CASCADE",
            ondelete="CASCADE"
        )
    )

    tagClass = relationship("tagClass", foreign_keys=[TagClassID_A])
    tag = relationship("tag", foreign_keys=[TagClassID_B])
  
class Message_hasTag(Base):
    __tablename__ = 'message_hasTag'

    messageID:Mapped[int] = mapped_column(BigInteger, ForeignKey('message.messageID'), primary_key=True)
    tagID:Mapped[int] = mapped_column(Integer, ForeignKey('tag.tagID'), primary_key=True)

    message = relationship("Message", backref="tags")
    tag = relationship("tag", backref="messages")

class Forum_hasTag(Base):
    __tablename__ = 'forum_hasTag'

    forumID:Mapped[int] = mapped_column(BigInteger, ForeignKey('forum.forumID'), primary_key=True)
    tagID:Mapped[int] = mapped_column(Integer, ForeignKey('tag.tagID'), primary_key=True)

    forum = relationship("Forum", backref="tags")
    tag = relationship("tag", backref="forums")

class Forum_hasMember(Base):
    __tablename__ = 'forum_hasMember'

    personID:Mapped[int] = mapped_column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    forumID:Mapped[int] = mapped_column(BigInteger, ForeignKey('forum.forumID'), primary_key=True)
    joinDate:Mapped[datetime.datetime] = mapped_column(TIMESTAMP)

    person = relationship("Person", backref="forums_joined")
    forum = relationship("Forum", backref="members")

class Person_likes_Message(Base):
    __tablename__ = 'person_likes_Message'

    personID:Mapped[int] = mapped_column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    messageID:Mapped[int] = mapped_column(BigInteger, ForeignKey('message.messageID'), primary_key=True)
    creationDate:Mapped[datetime.datetime] = mapped_column(TIMESTAMP)

    person = relationship("Person", back_populates="likes_messages")
    message = relationship("Message", back_populates="likes")

class Person_likes_Comment(Base):
    __tablename__ = 'person_likes_Comment'

    personID:Mapped[int] = mapped_column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    commentID:Mapped[int] = mapped_column(BigInteger, ForeignKey('comment.commentID'), primary_key=True)
    creationDate:Mapped[datetime.datetime] = mapped_column(TIMESTAMP)

    person = relationship("Person", back_populates="likes_comments")
    comment = relationship("Comment", backref="likes")

class Person_knows_Person(Base):
    __tablename__ = 'person_knows_Person'

    personID_A:Mapped[int] = mapped_column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    personID_B:Mapped[int] = mapped_column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    creationDate:Mapped[datetime.datetime] = mapped_column(TIMESTAMP)

    person_A = relationship("Person", foreign_keys=[personID_A])
    person_B = relationship("Person", foreign_keys=[personID_B])

class Person_hasinterest(Base):
    __tablename__ = 'person_hasinterest'

    personID:Mapped[int] = mapped_column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    tagID:Mapped[int] = mapped_column(Integer, ForeignKey('tag.tagID'), primary_key=True)

    person = relationship("Person", backref="interests")
    tag = relationship("tag", backref="people_interested")

class Organisation(Base):
    __tablename__ = 'organisation'
    
    organisationID:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String(255), nullable=False)
    url:Mapped[str] = mapped_column(String(2048))

    __mapper_args__ = {
        'polymorphic_identity': 'organisation',
        'polymorphic_on': organisationID
    }

class Company(Organisation):
    __tablename__ = 'company'

    companyID:Mapped[int] = mapped_column(Integer, ForeignKey('organisation.organisationID'), primary_key=True)
    countryID:Mapped[int] = mapped_column(Integer, ForeignKey('country.countryID'))

    __mapper_args__ = {
        "polymorphic_identity": "company",
    }
    
    extend_existing=True

class University(Organisation):
    __tablename__ = 'university'

    universityID:Mapped[int] = mapped_column(Integer, ForeignKey('organisation.organisationID'), primary_key=True)
    cityID:Mapped[int] = mapped_column(Integer, ForeignKey('city.cityID'))
    
    __mapper_args__ = {
        "polymorphic_identity": "university",
    }
    
    extend_existing=True

class StudyAt(Base):
    __tablename__ = 'studyAT'

    personID:Mapped[int] = mapped_column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    universityID:Mapped[int] = mapped_column(Integer, ForeignKey('university.universityID'), primary_key=True)
    classYear:Mapped[int] = mapped_column(SmallInteger, nullable=False)

    person = relationship("Person", backref="studies")
    university = relationship("University", backref="students")

class WorkAt(Base):
    __tablename__ = 'workAT'

    personID:Mapped[int] = mapped_column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    companyID:Mapped[int] = mapped_column(Integer, ForeignKey('company.companyID'), primary_key=True)
    workFrom:Mapped[int] = mapped_column(SmallInteger, nullable=False)

    person = relationship("Person", backref="works")
    company = relationship("Company", backref="employees")
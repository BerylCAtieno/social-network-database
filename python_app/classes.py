from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, BigInteger, SmallInteger, Date, TIMESTAMP
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint


class Base(DeclarativeBase):
    pass

class Place(Base):
    __tablename__ = 'place'
    
    placeID = Column(Integer, primary_key=True)
    name = Column(String(255))

    __mapper_args__ = {
        'polymorphic_identity': 'place',
        'polymorphic_on': placeID
    }
    

class Continent(Place):
    __tablename__ = 'continent'
    
    continentID = Column(Integer, ForeignKey('place.placeID'), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "continentID",
    }
    
    extend_existing=True

class Country(Place):
    __tablename__ = 'country'
    
    countryID = Column(Integer, ForeignKey('place.placeID'), primary_key=True)
    isPartOf = Column(Integer, ForeignKey('continent.continentID'))

    __mapper_args__ = {
        "polymorphic_identity": "countryID",
    }

    extend_existing=True

    continent = relationship("Continent")

class City(Place):
    __tablename__ = 'city'
    
    cityID = Column(Integer, ForeignKey('place.placeID'), primary_key=True)
    isPartOf = Column(Integer, ForeignKey('country.countryID'))

    __mapper_args__ = {
        "polymorphic_identity": "cityID",
    }

    extend_existing=True

    country = relationship("Country")

class Person(Base):
    __tablename__ = 'person'
    
    personID = Column(BigInteger, primary_key=True)
    firstName = Column(String(25), nullable=False)
    lastName = Column(String(25), nullable=False)
    gender = Column(String(25))
    birthday = Column(Date, nullable=False)
    creationDate = Column(TIMESTAMP)
    locationIP = Column(String(255))
    browserUsed = Column(String(255))
    cityID = Column(Integer, ForeignKey('city.cityID'))
    
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
    
    personID = Column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    email = Column(String(255), nullable=False, unique=True)

    person = relationship("Person", back_populates="emails")

class Language(Base):
    __tablename__ = 'language'
    
    personID = Column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    language = Column(String(255), nullable=False)

    person = relationship("Person", back_populates="languages")

class Forum(Base):
    __tablename__ = 'forum'
    
    forumID = Column(BigInteger, primary_key=True)
    title = Column(String(55))
    creationDate = Column(TIMESTAMP)
    moderatorID = Column(BigInteger, ForeignKey('person.personID'))

    moderator = relationship("Person", back_populates="forums")

class Message(Base):
    __tablename__ = 'message'
    
    messageID = Column(BigInteger, primary_key=True)
    content = Column(String(255))
    length = Column(Integer)
    creator = Column(BigInteger, ForeignKey('person.personID'))
    countryID = Column(BigInteger, ForeignKey('country.countryID'))
    creationDate = Column(TIMESTAMP)
    browserused = Column(String(55))
    locationIP = Column(String(55))

    __mapper_args__ = {
        'polymorphic_identity': 'message',
        'polymorphic_on': messageID
    }

    creator = relationship("Person", back_populates="messages")

class Post(Message):
    __tablename__ = 'post'

    postID = Column(BigInteger, ForeignKey('message.messageID'), primary_key=True)
    imageFile = Column(String(255))
    forumID = Column(BigInteger, ForeignKey('forum.forumID'))

    __mapper_args__ = {
        'polymorphic_identity': 'postID',
        'polymorphic_on': postID
    }

class Comment(Base):
    __tablename__ = 'comment'

    commentID = Column(BigInteger, primary_key=True)
    creationDate = Column(TIMESTAMP)
    locationIP = Column(String(50))
    browserUsed = Column(String(50))
    content = Column(String(255))
    length = Column(Integer)
    creator = Column(BigInteger)
    replyOfPost = Column(String(50))
    replyOfComment = Column(String(50))

class tag(Base):
    __tablename__ = 'tag'

    tagID = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(String(2048))

class tagClass(Base):
    __tablename__ = 'tagclass'

    tagClassID = Column(Integer, primary_key=True)
    tagClassName = Column(String(255))
    url = Column(String(2048))


class tagClass_isSubclassof(Base):
    __tablename__ = 'tagClass_isSubclassof'

    TagClassID_A = Column(Integer)
    TagClassID_B = Column(Integer)

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

    messageID = Column(BigInteger, ForeignKey('message.messageID'), primary_key=True)
    tagID = Column(Integer, ForeignKey('tag.tagID'), primary_key=True)

    message = relationship("Message", backref="tags")
    tag = relationship("tag", backref="messages")

class Forum_hasTag(Base):
    __tablename__ = 'forum_hasTag'

    forumID = Column(BigInteger, ForeignKey('forum.forumID'), primary_key=True)
    tagID = Column(Integer, ForeignKey('tag.tagID'), primary_key=True)

    forum = relationship("Forum", backref="tags")
    tag = relationship("tag", backref="forums")

class Forum_hasMember(Base):
    __tablename__ = 'forum_hasMember'

    personID = Column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    forumID = Column(BigInteger, ForeignKey('forum.forumID'), primary_key=True)
    joinDate = Column(TIMESTAMP)

    person = relationship("Person", backref="forums_joined")
    forum = relationship("Forum", backref="members")

class Person_likes_Message(Base):
    __tablename__ = 'person_likes_Message'

    personID = Column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    messageID = Column(BigInteger, ForeignKey('message.messageID'), primary_key=True)
    creationDate = Column(TIMESTAMP)

    person = relationship("Person", back_populates="likes_messages")
    message = relationship("Message", back_populates="likes")

class Person_likes_Comment(Base):
    __tablename__ = 'person_likes_Comment'

    personID = Column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    commentID = Column(BigInteger, ForeignKey('comment.commentID'), primary_key=True)
    creationDate = Column(TIMESTAMP)

    person = relationship("Person", back_populates="likes_comments")
    comment = relationship("Comment", backref="likes")

class Person_knows_Person(Base):
    __tablename__ = 'person_knows_Person'

    personID_A = Column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    personID_B = Column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    creationDate = Column(TIMESTAMP)

    person_A = relationship("Person", foreign_keys=[personID_A])
    person_B = relationship("Person", foreign_keys=[personID_B])

class Person_hasinterest(Base):
    __tablename__ = 'person_hasinterest'

    personID = Column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    tagID = Column(Integer, ForeignKey('tag.tagID'), primary_key=True)

    person = relationship("Person", backref="interests")
    tag = relationship("tag", backref="people_interested")

class Organisation(Base):
    __tablename__ = 'organisation'
    
    organisationID = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(String(2048))

    __mapper_args__ = {
        'polymorphic_identity': 'organisation',
        'polymorphic_on': organisationID
    }

class Company(Organisation):
    __tablename__ = 'company'

    companyID = Column(Integer, ForeignKey('organisation.organisationID'), primary_key=True)
    countryID = Column(Integer, ForeignKey('country.countryID'))

    __mapper_args__ = {
        "polymorphic_identity": "companyID",
    }
    
    extend_existing=True

class University(Organisation):
    __tablename__ = 'university'

    universityID = Column(Integer, ForeignKey('organisation.organisationID'), primary_key=True)
    cityID = Column(Integer, ForeignKey('city.cityID'))
    
    __mapper_args__ = {
        "polymorphic_identity": "universityID",
    }
    
    extend_existing=True

class StudyAt(Base):
    __tablename__ = 'studyAT'

    personID = Column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    universityID = Column(Integer, ForeignKey('university.universityID'), primary_key=True)
    classYear = Column(SmallInteger, nullable=False)

    person = relationship("Person", backref="studies")
    university = relationship("University", backref="students")

class WorkAt(Base):
    __tablename__ = 'workAT'

    personID = Column(BigInteger, ForeignKey('person.personID'), primary_key=True)
    companyID = Column(Integer, ForeignKey('company.companyID'), primary_key=True)
    workFrom = Column(SmallInteger, nullable=False)

    person = relationship("Person", backref="works")
    company = relationship("Company", backref="employees")
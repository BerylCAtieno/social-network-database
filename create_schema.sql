DROP SCHEMA if exists social_network_db CASCADE;
CREATE SCHEMA social_network_db;
SET search_path TO social_network_db;

-- Create Place, continent, country, city tables

CREATE TABLE place(
	placeID INT PRIMARY KEY,
	name VARCHAR (255)
);


CREATE TABLE continent(
	continentID INT,
	primary key (continentID),
    FOREIGN KEY (continentID) REFERENCES place(placeID) ON UPDATE NO ACTION ON DELETE CASCADE	
);

CREATE TABLE country( 
	countryID int PRIMARY KEY,
	isPartOf int NOT NULL,
	FOREIGN KEY (countryID) REFERENCES place(placeID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (isPartOf) REFERENCES continent(continentID) ON UPDATE CASCADE ON DELETE CASCADE
) ;

CREATE TABLE city(
	cityID int PRIMARY KEY,
	isPartOf int not null,
	FOREIGN KEY (cityID)REFERENCES place(placeID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (isPartOf) REFERENCES country(countryID) ON UPDATE CASCADE ON DELETE CASCADE	
);


-- Create Person Table

CREATE TABLE person (
	personID BIGINT PRIMARY KEY,
	firstName VARCHAR(25) NOT NULL,
	lastName VARCHAR(25)  NOT NULL,
	gender VARCHAR(25),
	birthday DATE ,
	creationDate TIMESTAMP check ( NOW()::timestamp > creationDate),
	locationIP  VARCHAR(255),
	browserUsed VARCHAR(255),
	cityID INT,
	FOREIGN KEY (cityID) REFERENCES city(cityID) ON UPDATE CASCADE ON DELETE CASCADE
);

-- pERSON eMAILS

CREATE TABLE personemail(
	 personID bigint,
	 email VARCHAR(255) UNIQUE NOT NULL CHECK ( email ~ '^[a-zA-Z0-9.!#$%&''*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$' ),
	 PRIMARY KEY (personID, email),
	 FOREIGN KEY (personID) REFERENCES PERSON(PERSONID) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Person Language
CREATE TABLE language (
	 languageID BIGINT,
	 language VARCHAR(255) NOT NULL,
	 PRIMARY KEY (languageID, language),
	 FOREIGN KEY (languageID) REFERENCES person(personID) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Forum
CREATE TABLE forum(
	forumID BIGINT PRIMARY KEY,
	title VARCHAR(55),
	creationDate TIMESTAMP ,
	moderatorID BIGINT ,
	FOREIGN KEY (moderatorID) REFERENCES person(personID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE "message"(
	messageID BIGINT PRIMARY KEY,
	"content" VARCHAR(255),
	"length" INT, 
	creator BIGINT ,
	countryID BIGINT,
	creationDate TIMESTAMP,
	browserused  VARCHAR(55),
	locationIP   VARCHAR(55),
	FOREIGN KEY (creator) REFERENCES person(personID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (countryID) REFERENCES country(countryID) ON UPDATE CASCADE ON DELETE CASCADE	
);

-- Post table
CREATE TABLE post(
	postID BIGINT PRIMARY KEY,
	imageFile varchar(255),
	forumID BIGINT ,
	FOREIGN KEY (postID) REFERENCES "message"(messageID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (forumID) REFERENCES forum(forumID) ON UPDATE CASCADE ON DELETE CASCADE
);

-- comment table

CREATE TABLE "comment"(
	commentID BIGINT PRIMARY KEY,
	replyOfPost BIGINT ,
	replyOfComment BIGINT,
	FOREIGN KEY (replyOfPost) REFERENCES post(postID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (replyOfComment) REFERENCES COMMENT(commentID) ON UPDATE CASCADE ON DELETE CASCADE
);

--tag and tag class tables

Create TABLE tag(
	tagID BIGINT PRIMARY KEY, 
	name VARCHAR(255) NOT NULL, 
	url VARCHAR (2048) 
);

CREATE TABLE tagClass(
	tagClassID int PRIMARY KEY ,
	tClassName varchar(255) not null, 
	url varchar(2048)  
);

CREATE TABLE tagClass_isSubclassof(
	TagClassID_A INT,
	TagClassID_B INT,
	PRIMARY KEY(TagClassID_A,TagClassID_B),
	FOREIGN KEY (TagClassID_A) REFERENCES tagClass(tagClassID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (TagClassID_B) REFERENCES tag(tagID) ON UPDATE CASCADE ON DELETE CASCADE
);


--Relationships to tag table
CREATE TABLE message_hasTag(
	messageID BIGINT ,
	tagID INT ,
	PRIMARY KEY (messageID, tagID),
	FOREIGN KEY (messageID) REFERENCES "message"(messageID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (tagID) REFERENCES tag(tagID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE forum_hasTag(
	forumID BIGINT ,
	tagID INT ,
	PRIMARY KEY (forumID, tagID),
	FOREIGN KEY (forumID) REFERENCES forum(forumID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (tagID) REFERENCES tag(tagID) ON UPDATE CASCADE ON DELETE CASCADE
);

-- forum-member relationship
CREATE TABLE forum_hasMember(
	personID BIGINT ,
	forumID  BIGINT ,
	joinDate TIMESTAMP , 
	PRIMARY KEY (forumID, personID),
	FOREIGN KEY (forumID) REFERENCES forum(forumID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (personID) REFERENCES person(personID) ON UPDATE CASCADE ON DELETE CASCADE
);

--person likes message

CREATE TABLE person_likes_Message(
	personID BIGINT,
	messageID BIGINT,
	creationDate TIMESTAMP,
	PRIMARY KEY (personID, messageID),
	FOREIGN KEY (messageID) REFERENCES "message"(messageID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (personID) REFERENCES person(personID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE person_knows_Person(
	personID_A BIGINT NOT NULL,
	personID_B BIGINT NOT NULL,
	creationDate TIMESTAMP NOT NULL,
	PRIMARY KEY (personID_A, personID_B),
	FOREIGN KEY (personID_B) REFERENCES "person"(personID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (personID_A) REFERENCES person(personID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Person_hasinterest(
	personID BIGINT ,
	tagID INT,    
	PRIMARY KEY (personID , tagID),
	FOREIGN KEY (personID) REFERENCES "person"(personID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (tagID) REFERENCES tag(tagID) ON UPDATE CASCADE ON DELETE CASCADE
);

--Organization tables

CREATE TABLE organisation(
	OrganisationID INT PRIMARY KEY,
	name VARCHAR(255) not null ,
	url VARCHAR(2048)	
);

CREATE TABLE university(
	universityID INT PRIMARY KEY,
	cityID INT ,
	FOREIGN KEY (universityID) REFERENCES Organisation(OrganisationID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (cityID) REFERENCES city(cityID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE company(
	companyID INT PRIMARY KEY,
	countryID INT ,
	FOREIGN KEY (companyID) REFERENCES Organisation(OrganisationID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (countryID) REFERENCES country(countryID) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Organization relationships

CREATE TABLE studyAT(
	personID BIGINT,
	universityID INT,
	classYear SMALLINT ,
	PRIMARY KEY (universityID, personID),
	FOREIGN KEY (personID) REFERENCES person(personID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (universityID) REFERENCES university(universityID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE workAT(
	personID BIGINT   ,
	companyID INT  ,
	workFrom SMALLINT   ,
	PRIMARY KEY (companyID, personID),
	FOREIGN KEY (personID) REFERENCES person(personID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (companyID) REFERENCES company(companyID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Place (
	PlaceID INT PRIMARY KEY NOT NULL,
    Name VARCHAR(255) NOT NULL
);

CREATE TABLE Continent (
	ContinentID INT PRIMARY KEY NOT NULL,
	Name VARCHAR(255),
    FOREIGN KEY (ContinentID) REFERENCES Place(PlaceID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Country (
	CountryID INT PRIMARY KEY NOT NULL,
	Name VARCHAR(255),
	IsPartOf INT,
    FOREIGN KEY (IsPartOf) REFERENCES Continent(ContinentID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE City (
	CityID INT PRIMARY KEY NOT NULL,
	Name VARCHAR(255),
	IsPartOf INT,
    FOREIGN KEY (IsPartOf) REFERENCES Country(CountryID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Person (
	PersonID BIGINT PRIMARY KEY NOT NULL,
	FirstName VARCHAR(50) NOT NULL,
	LastName VARCHAR(50) NOT NULL,
	Gender VARCHAR(50),
	Birthday TIMESTAMP CHECK (birthday <= CURRENT_DATE),
	CreationDate TIMESTAMP,
	BrowserUsed VARCHAR(50),
	Place INT,
	LocationIP VARCHAR(50),
	FOREIGN KEY (Place) REFERENCES Place(PlaceID)
);
	
CREATE TABLE PersonEmail (
	EmailID SERIAL PRIMARY KEY NOT NULL,
	PersonID BIGINT NOT NULL,
	Email VARCHAR(255) NOT NULL CHECK (Email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
	FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE PersonLanguage (
	PersonID BIGINT NOT NULL,
	Language VARCHAR(50),
	PRIMARY KEY (PersonID, Language),
	FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE PersonKnowsPerson (
    PersonID_A BIGINT NOT NULL,
    PersonID_B BIGINT NOT NULL,
	CreationDate TIMESTAMP,
    PRIMARY KEY (PersonID_A, PersonID_B),
    FOREIGN KEY (PersonID_A) REFERENCES Person(PersonID) ON DELETE CASCADE,
    FOREIGN KEY (PersonID_B) REFERENCES Person(PersonID) ON DELETE CASCADE
);

CREATE TABLE University (
	UniversityID INT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
	URL VARCHAR(255),
	Place INT,
	FOREIGN KEY (Place) REFERENCES Place(PlaceID)
	
);
CREATE TABLE Company (
	CompanyID INT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
	URL VARCHAR(255),
	Place INT,
	FOREIGN KEY (Place) REFERENCES Place(PlaceID)
);
CREATE TABLE PersonStudyAtUniversity(
	PersonID BIGINT NOT NULL,
    UniversityID INT NOT NULL,
    ClassYear INT,
    PRIMARY KEY (PersonID, UniversityID),
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE,
    FOREIGN KEY (UniversityID) REFERENCES University(UniversityID) ON DELETE CASCADE
);

CREATE TABLE PersonWorkAtCompany(
    PersonID BIGINT NOT NULL,
    CompanyID INT NOT NULL,
    WorkFrom INT,
    PRIMARY KEY (PersonID, CompanyID),
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE,
    FOREIGN KEY (CompanyID) REFERENCES Company(CompanyID) ON DELETE CASCADE
);
	
CREATE TABLE Forum (
	ForumID BIGINT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    CreateDate TIMESTAMP NOT NULL,
	Moderator BIGINT,
	FOREIGN KEY (Moderator) REFERENCES Person(PersonID)
);
	
CREATE TABLE ForumHasMember(
	ForumID BIGINT NOT NULL,
    PersonID BIGINT NOT NULL,
    JoinDate TIMESTAMP NOT NULL,
    PRIMARY KEY (ForumID, PersonID)
);

CREATE TABLE Post (
	PostID BIGINT PRIMARY KEY,
	ImageFile VARCHAR(50),
    CreationDate TIMESTAMP,
	LocationIP VARCHAR(50),
	BrowserUsed VARCHAR(50),
	Language VARCHAR(50),
    Content VARCHAR(255),
    Length INT,
	Creator BIGINT,
	ForumID BIGINT,
	Place INT,
    FOREIGN KEY (Creator) REFERENCES Person(PersonID),
    FOREIGN KEY (ForumID) REFERENCES Forum(ForumID),
    FOREIGN KEY (Place) REFERENCES Place(PlaceID)
);

CREATE TABLE Comment (
	CommentID BIGINT PRIMARY KEY,
    CreationDate TIMESTAMP,
	LocationIP VARCHAR(50),
	BrowserUsed VARCHAR(50),
	Content VARCHAR(255),
	Length INT,
	Creator BIGINT,
	Place INT
);
CREATE TABLE Tag (
	TagID INT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
	Url VARCHAR(255) NOT NULL
);

CREATE TABLE TagClass (
	TagClassID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
	Url VARCHAR(255) NOT NULL,
	FOREIGN KEY (TagClassID) REFERENCES Tag(TagID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE PostHasTag (
	PostID BIGINT NOT NULL,
    TagID INT NOT NULL,
    PRIMARY KEY (PostID, TagID),
    FOREIGN KEY (PostID) REFERENCES Post(PostID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (TagID) REFERENCES Tag(TagID) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE Tag_HasType_TagClass (
	TagID INT NOT NULL,
    TagClassID INT NOT NULL,
    PRIMARY KEY (TagID, TagClassID),
    FOREIGN KEY (TagID) REFERENCES Tag(TagID) ON DELETE CASCADE,
    FOREIGN KEY (TagClassID) REFERENCES TagClass(TagClassID) ON DELETE CASCADE
);
	
CREATE TABLE TagClass_issubclass_Tagclass (
	TagClassID_A INT NOT NULL,
	TagClassID_B INT NOT NULL,
	PRIMARY KEY (TagClassID_A, TagClassID_B),
	FOREIGN KEY (TagClassID_A) REFERENCES TagClass(TagClassID) ON DELETE CASCADE,
	FOREIGN KEY (TagClassID_B) REFERENCES TagClass(TagClassID) ON DELETE CASCADE
);

CREATE TABLE CommentHasTag (
	CommentID BIGINT NOT NULL,
	TagID INT NOT NULL,
	PRIMARY KEY (CommentID, TagID),
	FOREIGN KEY (CommentID) REFERENCES Comment(CommentID),
	FOREIGN KEY (TagID) REFERENCES Tag(TagID)
);

CREATE TABLE PersonLikesPost (
	PersonID BIGINT NOT NULL,
	PostID BIGINT NOT NULL,
	CreationDate TIMESTAMP,
	PRIMARY KEY (PersonID, PostID),
	FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (PostID) REFERENCES Post(PostID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE PersonLikesComment (
	PersonID BIGINT NOT NULL,
	CommentID BIGINT NOT NULL,
	CreationDate TIMESTAMP,
	PRIMARY KEY (PersonID, CommentID),
	FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (CommentID) REFERENCES Comment(CommentID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE PersonHasInterestTag (
	PersonID BIGINT NOT NULL,
	TagID INT NOT NULL,
	PRIMARY KEY (PersonID, TagID),
	FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (TagID) REFERENCES Tag(TagID) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE ForumHasTag (
	ForumID BIGINT NOT NULL,
	TagID INT NOT NULL,
	PRIMARY KEY (ForumID, TagID),
	FOREIGN KEY (ForumID) REFERENCES Forum(ForumID) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (TagID) REFERENCES Tag(TagID) ON DELETE CASCADE ON UPDATE CASCADE
);
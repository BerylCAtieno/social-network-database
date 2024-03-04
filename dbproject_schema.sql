-- Create Person table
CREATE TABLE Person (
    PersonID SERIAL PRIMARY KEY,
    CreationDate TIMESTAMP NOT NULL,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Gender VARCHAR(50),
    Birthday DATE CHECK (Birthday <= CURRENT_DATE),
    BrowserUsed VARCHAR(255),
    LocationIP VARCHAR(255)
);

-- Create Email table
CREATE TABLE PersonEmail (
    EmailID SERIAL PRIMARY KEY,
    PersonID INT NOT NULL,
    Email VARCHAR(255) NOT NULL CHECK (Email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create Language table
CREATE TABLE PersonLanguage (
    LanguageID SERIAL PRIMARY KEY,
    PersonID INT NOT NULL,
    Language VARCHAR(255) NOT NULL,
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create University table
CREATE TABLE University (
    UniversityID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
);

-- Create Company table
CREATE TABLE Company (
    CompanyID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
);

-- Create Person_StudyAt_University table
CREATE TABLE PersonStudyAtUniversity (
    PersonID INT NOT NULL,
    UniversityID INT NOT NULL,
    ClassYear INT,
    PRIMARY KEY (PersonID, UniversityID),
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE,
    FOREIGN KEY (UniversityID) REFERENCES University(UniversityID) ON DELETE CASCADE
);

-- Create Person_WorkAt_Company table
CREATE TABLE PersonWorkAtCompany (
    PersonID INT NOT NULL,
    CompanyID INT NOT NULL,
    WorkFrom INT,
    PRIMARY KEY (PersonID, CompanyID),
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE,
    FOREIGN KEY (CompanyID) REFERENCES Company(CompanyID) ON DELETE CASCADE
);

----cont.

-- Create Forum table
CREATE TABLE Forum (
    ForumID SERIAL PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    CreateDate TIMESTAMP NOT NULL
);


-- Create Post table (inherits Message)
CREATE TABLE Post (
    PostID SERIAL PRIMARY KEY,
    MessageID INT NOT NULL,
    Language VARCHAR(255),
    ImageFile VARCHAR(255),
    FOREIGN KEY (MessageID) REFERENCES Message(MessageID) ON DELETE CASCADE
);

-- Create Message table
CREATE TABLE Message (
    MessageID SERIAL PRIMARY KEY,
    CreationDate TIMESTAMP NOT NULL,
    BrowserUsed VARCHAR(255),
    LocationIP VARCHAR(255),
    Content TEXT,
    Length INT,
    PersonID INT NOT NULL,
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE
);

-- Create Comment table (inherits Message)
CREATE TABLE Comment (
    CommentID SERIAL PRIMARY KEY,
    MessageID INT NOT NULL,
    FOREIGN KEY (MessageID) REFERENCES Message(MessageID) ON DELETE CASCADE
);


-- Create Tag table
CREATE TABLE Tag (
    TagID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
);

-- Create TagClass table
CREATE TABLE TagClass (
    TagClassID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
);

-- Post_HasTag_Tag (Many-to-Many)
CREATE TABLE PostHasTag (
    PostID INT NOT NULL,
    TagID INT NOT NULL,
    PRIMARY KEY (PostID, TagID),
    FOREIGN KEY (PostID) REFERENCES Post(PostID) ON DELETE CASCADE,
    FOREIGN KEY (TagID) REFERENCES Tag(TagID) ON DELETE CASCADE
);

-- Tag_HasType_TagClass (Many-to-Many)
CREATE TABLE TagHasType (
    TagID INT NOT NULL,
    TagClassID INT NOT NULL,
    PRIMARY KEY (TagID, TagClassID),
    FOREIGN KEY (TagID) REFERENCES Tag(TagID) ON DELETE CASCADE,
    FOREIGN KEY (TagClassID) REFERENCES TagClass(TagClassID) ON DELETE CASCADE
);

-- Create Place, City, Country, and Continent tables, assuming City and Country inherit from Place
CREATE TABLE Place (
    PlaceID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
);

CREATE TABLE City (
    CityID INT NOT NULL,
    PlaceID SERIAL PRIMARY KEY,
    FOREIGN KEY (PlaceID) REFERENCES Place(PlaceID) ON DELETE CASCADE
);

CREATE TABLE Country (
    CountryID INT NOT NULL,
    PlaceID SERIAL PRIMARY KEY,
    FOREIGN KEY (PlaceID) REFERENCES Place(PlaceID) ON DELETE CASCADE
);

CREATE TABLE Continent (
    ContinentID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
);

-- Person_KNOWS_Person (Many-to-Many)
CREATE TABLE PersonKnowsPerson (
    PersonID_A INT NOT NULL,
    PersonID_B INT NOT NULL,
    PRIMARY KEY (PersonID_A, PersonID_B),
    FOREIGN KEY (PersonID_A) REFERENCES Person(PersonID) ON DELETE CASCADE,
    FOREIGN KEY (PersonID_B) REFERENCES Person(PersonID) ON DELETE CASCADE
);

-- Person_HasMember_Forum (Many-to-Many)
CREATE TABLE ForumHasMember (
    ForumID INT NOT NULL,
    PersonID INT NOT NULL,
    JoinDate TIMESTAMP NOT NULL,
    PRIMARY KEY (ForumID, PersonID),
    FOREIGN KEY (ForumID) REFERENCES Forum(ForumID) ON DELETE CASCADE,
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE
);

-- Note: Adjust data types and constraints as needed for your specific requirements.


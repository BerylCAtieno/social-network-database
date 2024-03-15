import pandas as pd
import psycopg2

def preprocess_data(data, datatype_mapping):
    for column, datatype in datatype_mapping.items():
        if column in data.columns:
            data[column] = data[column].astype(datatype)
    return data


def import_data(data, table_name, mapping, database_params):

    query = f"INSERT INTO {table_name} ({', '.join(mapping.keys())}) VALUES ({', '.join(['%s'] * len(mapping))})"
    
    try:
        connection = psycopg2.connect(**database_params)
        with connection.cursor() as cursor:
            for index, row in data.iterrows():
                values = [row[column] for column in mapping.values()]
                cursor.execute(query, values)
            connection.commit()
            print("Data insertion successful!")
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()



database_params = {
    "dbname": "social_2",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}  

#Data
Person = pd.read_csv("social_network/person_0_0.csv", sep='|')
PersonEmail = pd.read_csv("social_network/person_email_emailaddress_0_0.csv", sep='|')
PersonLanguage = pd.read_csv("social_network/person_speaks_language_0_0.csv", sep='|')
Organizations = pd.read_csv("social_network/organisation_0_0.csv", sep='|')
PersonStudyAtUniversity = pd.read_csv("social_network/person_studyAt_organisation_0_0.csv", sep='|')
PersonWorkAtCompany = pd.read_csv("social_network/person_workAt_organisation_0_0.csv", sep='|')
Forum = pd.read_csv("social_network/forum_0_0.csv", sep='|')
ForumHasMember = pd.read_csv("social_network/forum_hasMember_person_0_0.csv", sep='|')
ForumHasTag = pd.read_csv("social_network/forum_hasTag_tag_0_0.csv", sep='|')
Post = pd.read_csv("social_network/post_0_0.csv", sep='|')
Comment = pd.read_csv("social_network/comment_0_0.csv", sep='|')
Comment_hastag = pd.read_csv("social_network/comment_hasTag_tag_0_0.csv", sep='|')
Tag = pd.read_csv("social_network/tag_0_0.csv", sep='|')
TagClass = pd.read_csv("social_network/tagclass_0_0.csv", sep='|')
TagClass_isSubclass = pd.read_csv("social_network/tagclass_isSubclassOf_tagclass_0_0.csv", sep='|')
PostHasTag = pd.read_csv("social_network/post_hasTag_tag_0_0.csv", sep='|')
TagHasType = pd.read_csv("social_network/tag_hasType_tagclass_0_0.csv", sep='|')
Place = pd.read_csv("social_network/place_0_0.csv", sep='|')
PersonKnowsPerson = pd.read_csv("social_network/person_knows_person_0_0.csv", sep='|')
PersonHasInterest = pd.read_csv("social_network/person_hasInterest_tag_0_0.csv", sep='|')
PersonLikesComment = pd.read_csv("social_network/person_likes_comment_0_0.csv", sep='|')
PersonLikesPost = pd.read_csv("social_network/person_likes_post_0_0.csv", sep='|')



datatype_mapping = {
    
    'Person': {'id': 'int', 'firstName': 'str', 'lastName': 'str', 'gender': 'str', 'birthday': 'datetime64[ns]', 'creationDate': 'datetime64[ns]',
       'locationIP': 'str', 'browserUsed': 'str', 'place': 'int'},
    'PersonEmail': {'Person.id': 'int', 'email': 'str'},
    'PersonLanguage': {'Person.id': 'int', 'language': 'str'},
    'Organizations': {'id': 'int', 'type': 'str', 'name': 'str', 'url': 'str', 'place': 'int'},
    'PersonStudyAtUniversity': {'Person.id': 'int', 'Organisation.id': 'int', 'classYear': 'int'},
    'PersonWorkAtCompany': {'Person.id': 'int', 'Organisation.id': 'int', 'workFrom': 'int'},
    'Forum': {'id': 'int', 'title': 'str', 'creationDate': 'datetime64[ns]', 'moderator': 'int'},
    'ForumHasMember': {'Forum.id': 'int', 'Person.id': 'int', 'joinDate': 'datetime64[ns]'},
    'ForumHasTag': {'Forum.id': 'int', 'Tag.id': 'int'},
    'Post': {'id': 'int', 'imageFile': 'str', 'creationDate': 'datetime64[ns]', 'locationIP': 'str', 'browserUsed': 'str',
       'language': 'str', 'content': 'str', 'length': 'int', 'creator': 'int', 'Forum.id': 'int', 'place': 'int'},
    'Comment': {'id': 'int', 'creationDate': 'datetime64[ns]', 'locationIP': 'str', 'browserUsed': 'str', 'content': 'str', 'length': 'int',
       'creator': 'int', 'place': 'int', 'replyOfPost': 'int', 'replyOfComment;': 'int'},
    'Comment_hastag': {'Comment.id': 'int', 'Tag.id': 'int'},
    'Tag': {'id': 'int', 'name': 'str', 'url': 'str'},
    'TagClass': {'id': 'int', 'name': 'str', 'url': 'str'},
    'TagClass_isSubclass': {'TagClass.id': 'int', 'TagClass.id.1': 'int'},
    'PostHasTag': {'Post.id': 'int', 'Tag.id': 'int'},
    'TagHasType': {'Tag.id': 'int', 'TagClass.id': 'int'},
    'Place': {'id': 'int', 'name': 'str', 'url': 'str', 'type': 'str', 'isPartOf': 'int'},
    'PersonKnowsPerson': {'Person.id': 'int', 'Person.id.1': 'int', 'creationDate': 'datetime64[ns]'},
    'PersonHasInterest': {'Person.id': 'int', 'Tag.id': 'int'},
    'PersonLikesComment': {'Person.id': 'int', 'Comment.id': 'int', 'creationDate': 'datetime64[ns]'},
    'PersonLikesPost': {'Person.id': 'int', 'Post.id': 'int', 'creationDate': 'datetime64[ns]'}
}


sql_mapping = {

    'place': {'id': 'PlaceID', 'name': 'name'},
    'continent': {'id': 'continentID'},
    'country': {'id': 'countryID', 'isPartOf': 'isPartOf'},
    'city':{'id': 'cityID', 'isPartOf': 'isPartOf'},
    'person': {'id': 'personID', 'firstName': 'firstName', 'lastName': 'lastName', 'gender': 'gender', 'birthday': 'birthday', 'creationDate': 'creationDate',
       'locationIP': 'locationIP', 'browserUsed': 'browserUsed', 'place': 'cityID'},
    'personemail': {'Person.id': 'personID', 'email': 'email'},
    'language': {'Person.id': 'personID', 'language': 'language'},
    'forum': {'id': 'forumID', 'title': 'title', 'creationDate': 'creationDate', 'moderator': 'moderatorID'},
    'message': {'id': 'messageID', 'content': 'content', 
                'length': 'length', 'creator': 'creator', 
                'place': 'countryID','creationDate': 'creationDate', 
                'browserUsed': 'browserUsed', 'locationIP': 'locationIP'},
    'post': {'id': 'postID', 'imageFile': 'imageFile', 'Forum.id': 'ForumID'},
    'comment': {'id': 'CommentID', 'creationDate': 'creationDate', 
                'replyOfPost': 'replyOfPost', 'replyOfComment;': 'replyOfComment'},
    'tag': {'id': 'TagID', 'name': 'name', 'url': 'url'},
    'tagclass': {'id': 'tagClassID', 'name': 'tagClassName'},
    'tagClass_isSubclassof': {'TagClass.id': 'TagClassID_A', 'TagClass.id.1': 'TagClassID_B'},
    'message_hastag': {'Comment.id': 'messageID', 'Tag.id': 'tagID'},
    'forum_hastag': {'Post.id': 'forumID', 'Tag.id': 'tagID'},
    'forum_hasMember': {'Forum.id': 'forumID', 'Person.id': 'personID', 'joinDate': 'joinDate'},
    'person_likes_Message': {'Person.id': 'personID', 'Post.id': 'messageID', 'creationDate': 'creationDate'},
    'person_likes_Comment': {'Person.id': 'PersonID', 'Comment.id': 'CommentID', 'creationDate': 'creationDate'},
    'person_knows_Person': {'Person.id': 'PersonID_A', 'Person.id.1': 'PersonID_A', 'creationDate': 'creationDate'},
    'Person_hasinterest': {'Person.id': 'personID', 'Tag.id': 'tagID'},
    'organisation': {'id': 'OrganisationID', 'name': 'name', 'url': 'url'},
    'university': {'id': 'universityID', 'place': 'cityID'}, 
    'company': {'id': 'companyID', 'place': 'countryID'},
    'studyAT': {'Person.id': 'personID', 'Organisation.id': 'universityID', 'classYear': 'classYear'},
    'workAT': {'Person.id': 'personID', 'Organisation.id': 'companyID', 'workFrom': 'workFrom'}

}

Person = preprocess_data(Person, datatype_mapping)
PersonEmail = preprocess_data(PersonEmail, datatype_mapping)
PersonLanguage = preprocess_data(PersonLanguage, datatype_mapping)
Organizations = preprocess_data(Organizations, datatype_mapping)
PersonStudyAtUniversity = preprocess_data(PersonStudyAtUniversity, datatype_mapping)
PersonWorkAtCompany = preprocess_data(PersonWorkAtCompany, datatype_mapping)
Forum = preprocess_data(Forum, datatype_mapping)
ForumHasMember = preprocess_data(ForumHasMember, datatype_mapping)
ForumHasTag = preprocess_data(ForumHasTag, datatype_mapping)
Post = preprocess_data(Post, datatype_mapping)
Comment = preprocess_data(Comment, datatype_mapping)
Comment_hastag = preprocess_data(Comment_hastag, datatype_mapping)
Tag = preprocess_data(Tag, datatype_mapping)
TagClass = preprocess_data(TagClass, datatype_mapping)
TagClass_isSubclass = preprocess_data(TagClass_isSubclass, datatype_mapping)
PostHasTag = preprocess_data(PostHasTag, datatype_mapping)
TagHasType = preprocess_data(TagHasType, datatype_mapping)
Place = preprocess_data(Place, datatype_mapping)
PersonKnowsPerson = preprocess_data(PersonKnowsPerson, datatype_mapping)
PersonHasInterest = preprocess_data(PersonHasInterest, datatype_mapping)
PersonLikesComment = preprocess_data(PersonLikesComment, datatype_mapping)
PersonLikesPost = preprocess_data(PersonLikesPost, datatype_mapping)



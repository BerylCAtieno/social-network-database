import os
import numpy as np
import pandas as pd
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import register_adapter, AsIs


#Dataframes
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

#database details
database_params = {
    "dbname": "social_2",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}

def import_place_data(Place):
    continent_subset = Place[Place['type'] == 'continent']
    country_subset = Place[Place['type'] == 'country']
    city_subset = Place[Place['type'] == 'city']
    
    place_query = """INSERT INTO Place (
                    PlaceID, 
                    name) 
                    VALUES (%s, %s)"""
    continent_query = """INSERT INTO Continent (
                    ContinentID) 
                    VALUES (%s)"""
    country_query = """INSERT INTO Country (
                    CountryID,
                    IsPartOf) 
                    VALUES (%s, %s)"""
    city_query = """INSERT INTO City (
                    CityID,
                    IsPartOf) 
                    VALUES (%s, %s)"""
    
    try:
        connection = psycopg2.connect(**database_params)

        with connection.cursor() as cursor:
            for index, row in Place.iterrows():
                PlaceID_value = row['id']
                name_value = row['name']
                cursor.execute(place_query, (PlaceID_value, name_value))

            for index, row in continent_subset.iterrows():
                ContinentID_value = row['id']
                cursor.execute(continent_query, (ContinentID_value))

            for index, row in country_subset.iterrows():
                CountryID_value = row['id']
                IsPartOf_value = row['IsPartOf']
                cursor.execute(country_query, (CountryID_value, IsPartOf_value))

            for index, row in city_subset.iterrows():
                CityID_value = row['id']
                IsPartOf_value = row['isPartOf']
                cursor.execute(city_query, (CityID_value, IsPartOf_value))

            connection.commit()
            print("Data insertion successful!")
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()


def import_person_data(Person):
    
    Person['creationDate'] = pd.to_datetime(Person['creationDate'], errors='coerce')
    Person['birthday'] = pd.to_datetime(Person['birthday'], errors='coerce')

   
    query = """INSERT INTO Person (
                PersonID, 
                CreationDate, 
                FirstName, 
                LastName, 
                Gender, 
                Birthday, 
                BrowserUsed, 
                LocationIP,
                cityID) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    try:
        connection = psycopg2.connect(**database_params)

    
        with connection.cursor() as cursor:
        
            for index, row in Person.iterrows():
            
                PersonID_value = row['id']
                CreationDate_value = row['creationDate']
                FirstName_value = row['firstName']
                LastName_value = row['lastName']
                Gender_value = row['gender']
                Birthday_value = row['birthday']
                BrowserUsed_value = row['browserUsed']
                LocationIP_value = row['locationIP']
                cityID_value = row['place']
            
                cursor.execute(query, (PersonID_value,
                                CreationDate_value,
                                FirstName_value,
                                LastName_value,
                                Gender_value,
                                Birthday_value,
                                BrowserUsed_value,
                                LocationIP_value,
                                cityID_value))
                connection.commit()
                print("Data insertion successful!")
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()

def import_person_email(PersonEmail):
    
    query = """INSERT INTO PersonEmail (
    PersonID, 
    email) 
    VALUES (%s, %s)"""

    try:
        connection = psycopg2.connect(**database_params)
        
        with connection.cursor() as cursor:
            for index, row in PersonEmail.iterrows():
                PersonID_value = row['Person.id']
                Email_value = row['email']
            
                cursor.execute(query, (PersonID_value,
                                Email_value))
                connection.commit()
                print("Data insertion successful!")
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()

def import_language(PersonLanguage):

    query = """
            INSERT INTO PersonLanguage (
            PersonID,
            Language
        ) VALUES (%s, %s)
"""
    try:
        connection = psycopg2.connect(**database_params)

        with connection.cursor() as cursor:
    
            for index, row in PersonLanguage.iterrows():
                PersonID_value = row['Person.id']
                Language_value = row['language']
        
                cursor.execute(query, (PersonID_value,
                               Language_value))
                connection.commit()
                print("Data insertion successful!")
    
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()

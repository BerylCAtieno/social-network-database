import psycopg2
import csv

csv_files = {

    "comment": "social_network\comment_0_0.csv",
    "comment_hastag": "social_network\comment_hasTag_tag_0_0.csv",
    "forum": "social_network\forum_0_0.csv",
    "forum_has_member": "social_network\forum_hasMember_person_0_0.csv",
    "forum_has_tag": "social_network/forum_hasTag_tag_0_0.csv",
    "organisation": "social_network\organisation_0_0.csv",
    "person": "social_network\person_0_0.csv",
    "person_email": "social_network\person_email_emailaddress_0_0.csv",
    "person_interest": "social_network\person_hasInterest_tag_0_0.csv",
    "person_knows_person": "social_network\person_knows_person_0_0.csv",
    "person_likes_comment": "social_network\person_likes_comment_0_0.csv",
    "person_likes_post": "social_network\person_likes_post_0_0.csv",
    "person_speaks_language": "social_network\person_speaks_language_0_0.csv",
    "person_study_at": "social_network/person_studyAt_organisation_0_0.csv",
    "person_work_at": "social_network\person_workAt_organisation_0_0.csv",
    "place": "social_network\place_0_0.csv",
    "post": "social_network\post_0_0.csv",
    "post_has_tag": "social_network/post_hasTag_tag_0_0.csv",
    "tag": "social_network\tag_0_0.csv",
    "tag_class": "social_network\tagclass_0_0.csv",
    "tag_hastype_tagclass": "social_network\tag_hasType_tagclass_0_0.csv",
    "tagclass_subclass": "social_network\tagclass_isSubclassOf_tagclass_0_0.csv"
}

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="social_network_project",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL database:", e)
        return None

def import_person(conn, table, csv_file):

    with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)

            data = list(reader)

    pass



def file_imports():
    pass


def transform_person():
    pass

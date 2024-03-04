#Data import 

import csv
import psycopg2
import datetime

from jproperties import Properties


# Function to transform data
def transform_data(row):
     transformed_row = {
        'CreationDate': datetime.strptime(row['creationDate'], '%Y-%m-%dT%H:%M:%S.%f%z'),
        'FirstName': row['firstName'],
        'LastName': row['lastName'],
        'Gender': row['gender'],
        'Birthday': datetime.strptime(row['birthday'], '%Y-%m-%d').date(),
        'BrowserUsed': row['browserUsed'],
        'LocationIP': row['locationIP']
    }
    return transformed_row


# read db configuration from property file

configs = Properties()

with open('app-config.properties', 'rb') as config_file:

    configs.load(config_file)


connection = psycopg2.connect(

    host=localhost,

    database=postgres-project1,

    user=postgres,

    password=password,

)



connection.set_session(autocommit=True)


with open('your_file.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        transformed_row = transform_data(row)
        # Construct SQL statement for insertion
        insert_query = "INSERT INTO your_table (column1, column2) VALUES (%s, %s)"
        configs.execute(insert_query, (transformed_row['column1'], transformed_row['column2']))

# Commit transactions and close connection
connection.commit()
configs.close()
connection.close()







from sqlalchemy import create_engine

#database params
username = 'postgres'
password = 'password'
hostname = 'localhost'
port = '5432'  
database_name = 'social_2'
schema_name = 'social_network_db'

# Create db URL

database_url = f"postgresql://{username}:{password}@{hostname}:{port}/{database_name}?currentSchema={schema_name}"


#create engine object
engine = create_engine(database_url)




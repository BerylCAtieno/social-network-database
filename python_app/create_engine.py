from sqlalchemy import create_engine

#database params
username = 'social_2'
password = 'password'
hostname = 'localhost'
port = '5432'  
database_name = 'social_network_db'

# Create db URL
database_url = f"postgresql://{username}:{password}@{hostname}:{port}/{database_name}"

#create engine object
engine = create_engine(database_url)




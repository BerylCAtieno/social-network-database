from sqlalchemy import create_engine

#database params
username = 'postgres'
password = 'password'
hostname = 'localhost'
port = '5432'  
database_name = 'social_2'
dbschema = 'social_network_db'

# Create db URL

database_url = f"postgresql://{username}:{password}@{hostname}:{port}/{database_name}"


#create engine object
engine = create_engine(database_url, connect_args={'options': '-csearch_path={}'.format(dbschema)})




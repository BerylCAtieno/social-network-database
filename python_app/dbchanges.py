import psycopg2


database_params = {
    "dbname": "social_2",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}


script_path = 'dbchanges.sql'

try:
    
    connection = psycopg2.connect(**database_params)
    cursor = connection.cursor()


    with open(script_path, 'r') as f:
        sql_script = f.read()

    cursor.execute(sql_script)
    connection.commit()

    print("SQL script executed successfully!")

except psycopg2.Error as e:
    print(f"Error: {e}")

finally:
    if connection:
        connection.close()

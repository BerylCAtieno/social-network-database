import psycopg2
from psycopg2 import OperationalError

database_params = {
    "dbname": "social_2",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}

def test_connection():
    try:
        connection = psycopg2.connect(**database_params)
        cursor = connection.cursor()
        print("Connection to PostgreSQL successful!")
        cursor.close()
        connection.close()
    except OperationalError as e:
        print(f"Unable to connect to PostgreSQL: {e}")

if __name__ == "__main__":
    test_connection()

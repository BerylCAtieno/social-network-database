import psycopg2
from psycopg2 import OperationalError

def test_connection():
    try:
        # Replace these values with your PostgreSQL connection details
        connection = psycopg2.connect(
            dbname="social_2",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()
        print("Connection to PostgreSQL successful!")
        cursor.close()
        connection.close()
    except OperationalError as e:
        print(f"Unable to connect to PostgreSQL: {e}")

if __name__ == "__main__":
    test_connection()

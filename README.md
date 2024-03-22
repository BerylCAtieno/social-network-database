# SOCIAL NETWORK PROJECT

## Overview

## Part 1: Database Design and Data Import
The first step to creating a complete database application is database design. The primary objective is to convert [this UML diagram](https://old.dbs.uni-leipzig.de/file/schema.png) into a valid relational model and then translate it into an SQL script for PostgreSQL. The UML diagram defines the entities of an online social network and their relationships to each other. This part of the documentation covers the first step of the project, focusing on the creation of a conceptual diagram and the subsequent development of SQL scripts to implement the designed database schema.

### UML Diagram to Relational Model
The UML diagram serves as the foundation for the relational model. Each entity and relationship is mapped to tables and foreign keys in the relational schema. To develop the relational model, the entities, attributes, and relationships are identified in the UML diagram, the cardinality of the relationships was determined and appropriate tables developed. This [SQL Script](./database_design/create_schema.sql) File details the schema entities, relationships, datatypes, cardinality, and constraints. The schema is run in PostgreSQL using psycopg2, a popular PostgreSQL adapter for the Python programming language, as follows;

```python
import psycopg2

script_path = 'create_schema.sql'

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
```

### Data Import
The data in the [social_network](./social_network) folder represents the activity within the social network over a period of time. This data is imported into the above created PostgreSQL schema using psycopg2. Full data import code in the [import_data.py](./database_design/import_data.py) file. The data import follows these steps;

#### Preprocessing Function

The preprocess_data function preprocesses a Pandas DataFrame by converting columns to specified data types based on the provided datatype mapping. This function is particularly useful for ensuring that DataFrame columns are correctly typed before further analysis, visualization, or insertion into a database.

##### Function Signature
```python
def preprocess_data(data, datatype_mapping):
```
##### Parameters
- `data`: A Pandas DataFrame containing the data to be preprocessed.
- `datatype_mapping`: A dictionary specifying the mapping between DataFrame columns and desired data types. Keys are column names in the DataFrame, and values are the desired data types to which the columns should be converted.
##### Behavior
- Iterate Over Columns: The function iterates over each key-value pair in the datatype_mapping dictionary, where the key represents a column name in the DataFrame, and the value represents the desired data type for that column.
- Check Column Existence: For each column specified in the datatype_mapping, the function checks if the column exists in the DataFrame.
- Type Conversion: If the column exists in the DataFrame, the function converts the column to the specified data type using the astype method provided by Pandas.
- Return Preprocessed Data: The function returns the preprocessed DataFrame with columns converted to the specified data types.
##### Example Usage
```python
import pandas as pd

# Define DataFrame and datatype mapping
data = pd.DataFrame(...)
datatype_mapping = {
    "column1": "int64",
    "column2": "float64",
    "column3": "object"
}

# Preprocess data
preprocessed_data = preprocess_data(data, datatype_mapping)
```
#### Data Import Function
The import_data function is designed to insert data from a Pandas DataFrame into a PostgreSQL database table. It provides flexibility in handling different data types and mappings between DataFrame columns and database table columns. This function simplifies the process of importing data into a PostgreSQL database while maintaining compatibility with different data types.
#### Function Signature
```python
def import_data(data, table_name, mapping, database_params):
```
##### Parameters
- `data`: A Pandas DataFrame containing the data to be inserted into the database.
- `table_name`: A string representing the name of the target database table where the data will be inserted.
- `mapping`: A dictionary specifying the mapping between DataFrame columns and database table columns. Keys are column names in the SQL table, and values are corresponding column names in the Pandas Dataframe.
- `database_params`: A dictionary containing parameters required to establish a connection to the PostgreSQL database, such as database name, user, password, host, and port.

##### Behavior
- Register Adapters: This function registers adapters for NumPy data types (np.int64 and np.int32). This step is essential to ensure compatibility with the PostgreSQL data types during data insertion.
- Query Construction: Constructs an SQL INSERT query dynamically based on the provided table name and column mappings.
- Database Connection: Establishes a connection to the PostgreSQL database using the provided database parameters.
- Setting Schema: Sets the search path to the specified schema name (social_network_db). This step ensures that the subsequent SQL operations are performed within the specified schema.
- Data Insertion: Iterates over each row in the DataFrame, extracts values based on the provided column mappings, and executes the SQL INSERT query to insert data into the database table.
- Committing Changes: Commits the transaction to save the changes made to the database.
- Error Handling: Handles any potential errors that may occur during the data insertion process and prints an error message if an exception is raised.
- Connection Closure: Closes the database connection to release resources after the data insertion process is complete.

##### Example Usage
```python
import pandas as pd
import psycopg2
import numpy as np

# Define database parameters
database_params = {
    "dbname": "your_database",
    "user": "your_username",
    "password": "your_password",
    "host": "your_host",
    "port": "your_port"
}

# Define DataFrame and mappings
data = pd.DataFrame(...)
mapping = {...}

# Import data into the database
import_data(data, "target_table", mapping, database_params)

```

## Part 2: SQL Queries, Views, and Triggers

This part of the project on creating views and executing various queries on the database created in Part 1. 
All SQL statements for this part included in [views_queries.sql](.\Views and Queries\views_queries.sql)
Here's a breakdown of what was accomplished:

### Part 2(a): View Creation

To facilitate handling of friendship relationships, which were stored as directed relationships, I created a view named pkp_symmetric. This view contains both directions of the friendship relationship, making it easier to execute queries related to friendships.

### Part 2(b): Queries
1. **Count of European Cities with Universities**: Identified the number of different European cities where universities are located.

2. **Forum Posts Authored by the Youngest Person**: Determined the number of forum posts authored by the youngest person in the database.

3. **Comments on Posts by Country**: Calculated the number of comments on posts from each country.

4. **Cities with Most Users**: Identified the cities from which the most users originate.

5. **Friends of 'Hans Johansson'**: Listed individuals who are friends with 'Hans Johansson'.

6. **Real Friends-of-a-Friend of 'Hans Johansson'**: Identified the "real" friends-of-a-friend of 'Hans Johansson'.

7. **Users in Forums with 'Mehmet Koksal'**: Determined users who are members of all forums where 'Mehmet Koksal' is also a member.

8. **Distribution of Users by Continent**: Provided the percentage distribution of users based on their continent of origin.

9. **Forums with More Posts Than Average**: Listed forums with more posts than the average number of posts across all forums.

10. **Persons Friends with Most Liked Post Creator**: Identified persons who are friends with the creator of the most liked post.

11. **Connected Persons to 'Jun Hu'**: Identified persons directly or indirectly connected to 'Jun Hu' (friends) and provided the minimum distance to 'Jun Hu'.

12. **Extended Connected Persons Query**: Extended the previous query to also output the minimum path between connected users.

### Part 2(c): Database Changes
Implemented a mechanism to document the termination of employment relationships, deleting corresponding entries in the `workAt` table and logging these deletions in a separate table named `Former_employees_table`.

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

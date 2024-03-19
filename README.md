# sOCIAL NETWORK PROJECT

## Overview

## Part 1: Database Design and Data Import
The first step to creating a complete database application is database design. The primary objective is to convert [this UML diagram](https://old.dbs.uni-leipzig.de/file/schema.png) into a valid relational model and then translate it into an SQL script for PostgreSQL. The UML diagram defines the entities of an online social network and their relationships to each other. This part of the documentation covers the first step of the project, focusing on the creation of a conceptual diagram and the subsequent development of SQL scripts to implement the designed database schema.

### UML Diagram to Relational Model
The UML diagram serves as the foundation for the relational model. Each entity and relationship is mapped to tables and foreign keys in the relational schema. To develop the relational model, the entities, attributes, and relationships are identified in the UML diagram, the cardinality of the relationships was determined and appropriate tables developed. This [SQL Script](./create_schema.sql) File details the schema entities, relationships, datatypes, cardinality, and constraints. The schema is run in PostgreSQL using psycopg2, a popular PostgreSQL adapter for the Python programming language, as follows;

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
The data in the [social_network](./social_network) folder represents the activity within the social network over a period of time. This data is imported into the above created PostgreSQL schema using psycopg2. Full data import code in the [import_data.py](./import_data.py) file. The data import follows these steps;

1. Import Libraries for Data Processing and Loading
```python
import pandas as pd
import numpy as np 
import psycopg2
from psycopg2.extensions import register_adapter, AsIs
```
2. Import data as Pandas dataframes
3. Datatype mapping
4. SQL Tables Mappings
5. Preprocessing Function
6. Data Import Function
7. Application


import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create a database connection."""
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Replace with your host
            database='schema',  # Replace with your database name
            user='',  # Replace with your MySQL username
            password=''  # Replace with your MySQL password
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
            return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def init_db():
    """Initialize the database with required tables."""
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor()
        with open('schema.sql', 'r') as file:
            sql_script = file.read()
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        connection.commit()
        cursor.close()
        connection.close()
        print("Database initialized successfully")

# Run the init_db function to initialize the database
init_db()

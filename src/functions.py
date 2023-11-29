import pyodbc


class DatabaseAccessException(Exception):
    "Raised when database connection can not be established"


def execute_statement(query: str) -> bool:
    "Will execute and commit a statement to the table specified. Returns true if it has been successful"
    try:
        connection = pyodbc.connect(
            Trusted_Connection="yes",
            driver="{SQL Server}",
            server="localhost\SQLEXPRESS",
            database="trades",
        )
        cursor = connection.cursor()
    except:
        # Raise an error if database can not be reached
        raise DatabaseAccessException("Could not connect to the database")
    try:
        # Attempt the query
        cursor.execute(query)
        connection.commit()
        connection.close()
        return True
    except pyodbc.ProgrammingError as e:
        # If query invalid, throw error
        connection.close()  # Make sure connection to database is closed
        print(e)
        return False


def select_statement(query: str) -> list:
    "Will execute and return data from a select statement"
    try:
        connection = pyodbc.connect(
            Trusted_Connection="yes",
            driver="{SQL Server}",
            server="localhost\SQLEXPRESS",
            database="trades",
        )
        cursor = connection.cursor()
    except:
        # Raise an error if database can not be reached
        raise DatabaseAccessException("Could not connect to the database")
    try:
        # Attempt the query
        cursor.execute(query)
        return_data = cursor.fetchall()[0][0]
        connection.close()
        return return_data
    except pyodbc.ProgrammingError as e:
        # If query invalid, throw error
        connection.close()  # Make sure connection to database is closed
        print(e)
        return "Error"

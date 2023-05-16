import mysql.connector
# from config import USER, PASSWORD, HOST - this keeps not picking up the separate file with my details
HOST = "localhost"
USER = "root"
PASSWORD = "ConservationSensation2"

class DbConnectionError(Exception):
    pass


def _connect_to_db(db_name):
    try:
       cnx = mysql.connector.connect(
           host=HOST,
           user=USER,
           password=PASSWORD,
           auth_plugin='mysql_native_password',
           database=db_name
       )
       return cnx
    except Exception as e:
        print(f'failed to connect + {str(e)}')

#combined function to view entries in the tables
def get_all_to_read(table):
    try:
        db_name = 'Bookapp'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print(f"Connected to DB: {db_name}")

        query = f"""SELECT title, author, series, book_type
                FROM {table}
                ORDER BY title;"""
        cur.execute(query)
        result = cur.fetchall()

        for i in result:
            print(i)
        cur.close()

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

# can get table results as separate functions rather than by inputting the table into the function
def get_all_read():
    try:
        db_name = 'Bookapp'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print(f"Connected to DB: {db_name}")

        query = """SELECT tr.title, tr.author, tr.series, tr.book_type
                FROM books_read r
                ORDER BY tr.title;"""
        cur.execute(query)
        result = cur.fetchall()

        for i in result:
            print(i)
        cur.close()

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

def insert_new_record(table):
    try:
        db_name = 'Bookapp'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print(f"Connected to DB: {db_name}")

        # not sure what format the data from the api will be in to add it to the query
        query = f"""INSERT INTO {table} ('title', 'author', 'series', 'book_type', 'lexile_min', 'lexile_max') VALUES ('{}', '{}', '{}', '{}', {}, {}, {})""")
        cur.execute(query)
        db_connection.commit()
        cur.close()


    except Exception as e:
        print(f"Error raised - {str(e)}")
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

    print(f"Your book has been added to {table}.")

# function to add a review to read books
def update_review( rating, book_title):
    try:
        db_name = 'tests'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print(f"Connected to DB: {db_name}")

        query = f"""
                UPDATE book_read         
                SET star_rating = '{rating}'
                WHERE title = '{book_title}'
        """
        cur.execute(query)
        db_connection.commit()

        cur.close()
        print(f'Your rating has been added to {book_title}')

    except Exception as e:
        print(f"Error raised = {str(e)}")
        raise DbConnectionError("Failed to read from the database")
    finally:
        if db_connection:
            db_connection.close()
            print('Database connection is closed')
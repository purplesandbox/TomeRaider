import mysql.connector
from tabulate import tabulate
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

#combined function to view entries in the tables this version just prints results
# def get_all_books(table):
#     try:
#         db_name = 'Bookapp'
#         db_connection = _connect_to_db(db_name)
#         cur = db_connection.cursor()
#         # probably want to remove this print and the DB closed print in the end but handy at the mo to check it works
#         print(f"Connected to DB: {db_name}")
#
#         if table == 'to_read_books':
#             query = f"""SELECT title, author, category
#                             FROM {table}
#                             ORDER BY title;"""
#         else:
#             query = f"""SELECT title, author, category, star_rating
#                 FROM {table}
#                 ORDER BY title;"""
#         cur.execute(query)
#         result = cur.fetchall()
#
#         for i in result:
#             print(i)
#         cur.close()
#
#     except Exception:
#         raise DbConnectionError("Failed to read data from DB")
#
#     finally:
#         if db_connection:
#             db_connection.close()
#             print("DB connection is closed")

#this version of get_all_books function prints results in a table
def get_all_books(table):
    try:
        db_name = 'Bookapp'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print(f"Connected to DB: {db_name}")

        if table == 'to_read_books':
            query = f"""SELECT title, author, category
                            FROM {table}
                            ORDER BY title;"""
        else:
            query = f"""SELECT title, author, category, star_rating
                FROM {table}
                ORDER BY title;"""
        cur.execute(query)
        result = cur.fetchall()

        # Convert the result to a list of lists
        data = [list(row) for row in result]

        # Print the table
        headers = ["Title", "Author", "Category"]
        if table != 'to_read_books':
            headers.append("Star Rating")
        print(tabulate(data, headers, tablefmt="grid"))

        cur.close()

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")
get_all_books('read_books')
# can get table results as separate functions rather than by inputting the table into the function
# def get_all_read():
#     try:
#         db_name = 'Bookapp'
#         db_connection = _connect_to_db(db_name)
#         cur = db_connection.cursor()
#         print(f"Connected to DB: {db_name}")
#
#         query = """SELECT tr.title, tr.author, tr.series, tr.book_type
#                 FROM books_read r
#                 ORDER BY tr.title;"""
#         cur.execute(query)
#         result = cur.fetchall()
#
#         for i in result:
#             print(i)
#         cur.close()
#
#     except Exception:
#         raise DbConnectionError("Failed to read data from DB")
#
#     finally:
#         if db_connection:
#             db_connection.close()
#             print("DB connection is closed")



def insert_book(table, title, author, category):
    try:
        db_name = 'Bookapp'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print(f"Connected to DB: {db_name}")
        # not sure what format the data from the api will be in to add it to the query
        query = f"""INSERT INTO {table} (title, author, category) VALUES ('{title}', '{author}', '{category}')"""
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

    print(f"{title} has been added to {table}.")


# insert_new_record('to_read_books', 'The Great Gatsby', 'F.Scott Fitzgerald', 'Literary Fiction')
# get_all_entries('to_read_books')
# function to add a review to read books
def update_review(book_title, rating):
    try:
        db_name = 'Bookapp'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print(f"Connected to DB: {db_name}")

        query = f"""
                UPDATE read_books
                SET star_rating = '{rating}'
                WHERE title = '{book_title}'
        """
        cur.execute(query)
        db_connection.commit()

        cur.close()
        print(f'Your rating has been added to {book_title}')

    except Exception as e:
        print(f"Error raised = {str(e)}")

def delete_book(table, book_title):
    try:
        db_name = 'Bookapp'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print(f"Connected to DB: {db_name}")

        query = f"""
                DELETE FROM {table}
                WHERE title = '{book_title}'      
        """
        cur.execute(query)
        db_connection.commit()

        cur.close()
        print(f'{book_title} has been deleted from {table}')

    except Exception as e:
        print(f"Error raised = {str(e)}")
# insert_book('read_books', 'The Great Gatsby', 'F.Scott Fitzgerald', 'Literary Fiction')
# update_review('The Great Gatsby', '5')
# get_all_entries('read_books')

def move_book(book_title): # doesn't take it off the to-read table
    try:
        db_name = 'Bookapp'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print(f"Connected to DB: {db_name}")

        query = f"""
                INSERT INTO read_books (title, author, category)
                SELECT title, author, category
                FROM to_read_books
                WHERE title = '{book_title}';"""
        cur.execute(query)
        db_connection.commit()

        cur.close()
        print(f'{book_title} has been moved to your Read Books!')

    except Exception as e:
        print(f"Error raised = {str(e)}")

move_book('The Hobbit')
get_all_books('read_books')
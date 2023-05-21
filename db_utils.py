import mysql.connector
from tabulate import tabulate
# from config import USER, PASSWORD, HOST

HOST = "localhost"
USER = "root"
PASSWORD = "yellowdolphin22!!"


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


# combined function to view entries in the tables, this version just prints results
def get_all_books(table):
    try:
        db_name = 'TomeRaider'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        # probably want to remove this print and the DB closed print in the end but handy at the mo to check it works
        print(f"Connected to DB: {db_name}")

        if table == 'to_read_books':
            query = f"""SELECT title, author, category
                            FROM {table}
                            ORDER BY title;"""
        else:
            query = f"""SELECT title, author, category, review, star_rating
                FROM {table}
                ORDER BY title;"""
        cur.execute(query)
        result = cur.fetchall()
        read_books = []

        for i in result:
            read_books.append(i)
        cur.close()
        return read_books

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


# print(get_all_books('to_read_books'))

# this version of get_all_books function prints results in a table
# def get_all_books(table):
#     try:
#         db_name = 'Bookapp'
#         db_connection = _connect_to_db(db_name)
#         cur = db_connection.cursor()
#         print(f"Connected to DB: {db_name}")
#
#         if table == 'to_read_books':
#             query = f"""SELECT title, author, category
#                             FROM {table}
#                             ORDER BY title;"""
#         else:
#             query = f"""SELECT title, author, category,review, star_rating
#                 FROM {table}
#                 ORDER BY title;"""
#         cur.execute(query)
#         result = cur.fetchall()
#
#         # Convert the result to a list of lists
#         data = [list(row) for row in result]
#
#         # Print the table
#         headers = ["Title", "Author", "Category"]
#         if table != 'to_read_books':
#             headers.append("Review")
#             headers.append("Star Rating")
#         return tabulate(data, headers, tablefmt="grid")
#
#         cur.close()
#
#     except Exception:
#         raise DbConnectionError("Failed to read data from DB")
#
#     finally:
#         if db_connection:
#             db_connection.close()
#             print("DB connection is closed")

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
        db_name = 'TomeRaider'
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


# for the following functions, if there are duplicate entries the function will apply to all
# function to add a review to read books
def update_rating(book_title, rating):
    try:
        db_name = 'TomeRaider'
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
        print(f'Your Star rating has been added to {book_title}')

    except Exception as e:
        print(f"Error raised = {str(e)}")


def update_review(book_title, review):  # review can be max 16,777,215 characters
    try:
        db_name = 'TomeRaider'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print(f"Connected to DB: {db_name}")

        query = f"""
                UPDATE read_books
                SET review = '{review}'
                WHERE title = '{book_title}'
        """
        cur.execute(query)
        db_connection.commit()

        cur.close()
        print(f'Your review has been added to {book_title}')

    except Exception as e:
        print(f"Error raised = {str(e)}")


def delete_book(table, book_title):
    try:
        db_name = 'TomeRaider'
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
# update_review('The Great Gatsby', 'It was great.')


def move_book(book_title):  # doesn't take it off the to-read table
    try:
        db_name = 'TomeRaider'
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


# move_book('The Hobbit')
# get_all_books('read_books')

def move_book2(book_title):  # does remove the book from the to-read table
    try:
        db_name = 'TomeRaider'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print(f"Connected to DB: {db_name}")

        # Query to insert the book into the 'read_books' table
        query_insert = f"""
            INSERT INTO read_books (title, author, category)
            SELECT title, author, category
            FROM to_read_books
            WHERE title = '{book_title}';"""
        cur.execute(query_insert)
        db_connection.commit()

        # Query to delete the book from the 'to_read_books' table
        query_delete = f"""
            DELETE FROM to_read_books
            WHERE title = '{book_title}';"""
        cur.execute(query_delete)
        db_connection.commit()

        cur.close()
        print(f'{book_title} has been moved to your Read Books!')

    except Exception as e:
        print(f"Error raised = {str(e)}")

# update_review('The Great Gatsby', "The plot itself is slow.\n In a time before authors cared more plot\n and cared more about how their book was written")
# update_rating('The Hobbit', '4')
# delete_book('read_books', 'The Hobbit')
# get_all_books('read_books')

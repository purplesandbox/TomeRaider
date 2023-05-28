import mysql.connector
from src.Database.config import USER, PASSWORD, HOST


class DbConnectionError(Exception):
    pass

# function to connect to the database
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


# combined function to view entries in the tables
def get_all_books(table):
    try:
        db_name = 'TomeRaider'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

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



# function to add book to either table
def insert_book(table, title, author, category):
    try:
        db_name = 'TomeRaider'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

        title = title.replace('"', '\\"')  # removing " and ' from titles

        query = f"""INSERT INTO {table} (title, author, category) VALUES ("{title}", "{author}", "{category}")"""
        cur.execute(query)
        db_connection.commit()
        cur.close()

    except Exception as e:
        print(f"Failed to insert book - {str(e)}")
        raise DbConnectionError(f"Failed to insert book: {str(e)}")

    finally:
        if db_connection:
            db_connection.close()


    print(f"{title} has been added to {table}.")
    return True

# for the following functions, if there are duplicate entries in table the function will apply to all
# function to add a rating to read_books table
def update_rating(book_title, rating):
    try:
        db_name = 'TomeRaider'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

        book_title = book_title.replace('"', '\\"')  # removing " and ' from titles

        query = f"""
                UPDATE read_books
                SET star_rating = '{rating}'
                WHERE title = "{book_title}"
        """
        cur.execute(query)
        db_connection.commit()

        cur.close()
        print(f"Your Star rating has been added to {book_title}")
        return True

    except Exception as e:
        raise DbConnectionError(f"Failed to update rating: {str(e)}")
        print(f"Failed to update rating: {str(e)}")

    finally:
        if db_connection:
            db_connection.close()


# function to add a review to read_books table
def update_review(book_title, review):  # review can be max 16,777,215 characters
    try:
        db_name = 'TomeRaider'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

        review = review.replace('"', '\\"')  # removing " and ' from reviews

        query = f"""
                UPDATE read_books
                SET review = "{review}"
                WHERE title = "{book_title}"
        """

        cur.execute(query)
        db_connection.commit()

        cur.close()
        print(f"Your review has been added to {book_title}")
        return True

    except Exception as e:
        raise DbConnectionError(f"Failed to update review: {str(e)}")
        print(f"Error raised = {str(e)}")

    finally:
        if db_connection:
            db_connection.close()



# function to delete a book from either table
def delete_book(table, book_title):
    try:
        db_name = 'TomeRaider'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

        book_title = book_title.replace('"', '\\"')  # removing " and ' from titles

        query = f"""
                DELETE FROM {table}
                WHERE title = "{book_title}"
        """
        cur.execute(query)
        db_connection.commit()

        cur.close()
        return True

    except Exception as e:
        raise DbConnectionError(f"Failed to delete book: {str(e)}")
        print(f"Error raised = {str(e)}")

    finally:
        if db_connection:
            db_connection.close()


""""
move_book is part of our expansion plans, and it's not currently implemented in the programme
"""""


def move_book(book_title):  # doesn't take it off the to-read table
    try:
        db_name = 'TomeRaider'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

        book_title = book_title.replace('"', '\\"') # removing " and ' from titles

        query = f"""
                INSERT INTO read_books (title, author, category)
                SELECT title, author, category
                FROM to_read_books
                WHERE title = "{book_title}";"""
        cur.execute(query)
        db_connection.commit()

        cur.close()
        print(f"{book_title} has been moved to your Read Books!")

    except Exception as e:
        print(f"Error raised = {str(e)}")

    finally:
        if db_connection:
            db_connection.close()



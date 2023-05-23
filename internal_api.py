from flask import Flask, jsonify
from API_results import BookAppAPI
import db_utils

app = Flask(__name__)


# Note: For category, the user has to input each word starting with a capital letter. The API will return an error
# as it is case-sensitive

class BookAlreadyOnTable(Exception):
    pass


class BookNotFound(Exception):
    pass


class NoSearchResultsWithGivenCriteria(Exception):
    pass


class InternalAPI:
    def __init__(self):
        self.book_app_api = BookAppAPI()

    # function to remove anything from the dictionary that is empty. Cleans up the user input
    def clean_user_input(self, user_input):
        return {k: v for k, v in user_input.items() if v != ''}

    # def search_book_suggestions(self, user_input):
    #     user_input = self.clean_user_input(user_input)
    #     book_suggestions = self.book_app_api.get_filtered_results(user_input)
    #     return book_suggestions

    def search_book_suggestions(self, user_input):

        x = user_input['book_num']
        user_input['book_num'] = 50
        user_input = self.clean_user_input(user_input)
        book_suggestions = self.book_app_api.get_filtered_results(user_input)

        # check for duplicates from read_list and return the number the person wanted
        unique_book_suggestions = self.check_for_duplicates_from_read_list(book_suggestions)

        unique_book_suggestions = self.check_for_duplicates_from_to_read_list(x, unique_book_suggestions)

        if unique_book_suggestions == []:
            raise NoSearchResultsWithGivenCriteria(
                'No search results that are not already on the read or to-read lists')
        # Return book suggestion
        return unique_book_suggestions
        # print this in user interactions class

    # function to give out a list of books with none of them being in the read_books section
    def check_for_duplicates_from_read_list(self, book_suggestions):
        book_list = db_utils.get_all_books('read_books')
        # a list of all the titles in the to_read_books list
        titles_in_read_list = [book[0] for book in book_list]
        # repeat_books is a list of book titles that have been suggested but are also in the to_read_books list
        book_suggestions = [book_suggestion for book_suggestion in book_suggestions if
                            book_suggestion['title'] not in titles_in_read_list]

        return book_suggestions

    def check_for_duplicates_from_to_read_list(self, x, book_suggestions):
        book_list = db_utils.get_all_books('to_read_books')
        # a list of all the titles in the to_read_books list
        titles_in_to_read_list = [book[0] for book in book_list]
        # repeat_books is a list of book titles that have been suggested but are also in the to_read_books list
        book_suggestions = [book_suggestion for book_suggestion in book_suggestions if
                            book_suggestion['title'] not in titles_in_to_read_list]

        return book_suggestions[:x]

    def random_book_suggestion(self, user_input):
        user_input = self.clean_user_input(user_input)
        random_book = self.book_app_api.get_random_result(user_input)
        # Convert authors and categories lists to strings
        random_book['authors'] = ', '.join(random_book['authors'])
        random_book['categories'] = ', '.join(random_book['categories'])

        # Return random_book
        return random_book

    def check_random_suggestion_in_to_read_list(self, random_book):
        book_list = db_utils.get_all_books('to_read_books')
        # a list of all the titles in the to_read_books list
        titles_in_to_read_list = [book[0] for book in book_list]
        # repeat_books is a list of book titles that have been suggested but are also in the to_read_books list
        if random_book['title'] in titles_in_to_read_list:
            return True
        else:
            return False

    def check_random_suggestion_in_read_list(self, random_book):
        book_list = db_utils.get_all_books('read_books')
        # a list of all the titles in the to_read_books list
        titles_in_read_list = [book[0] for book in book_list]
        # repeat_books is a list of book titles that have been suggested but are also in the to_read_books list
        if random_book['title'] in titles_in_read_list:
            return True
        else:
            return False

    def add_to_to_read_list(self, to_read):
        # to_read should be a dictionay coming from the user interactions where it gives the author, title, etc
        # check if book is already on the list. If it is an exception is raised
        book_list = db_utils.get_all_books('to_read_books')
        titles_in_to_read_list = (book[0] for book in book_list)
        if to_read['title'] in titles_in_to_read_list:
            raise BookAlreadyOnTable('This book is already on the to read list')

        # Call function to add book to reading list
        db_utils.insert_book(table='to_read_books', title=to_read['title'], author=to_read['authors'],
                             category=to_read['categories'])

        # Return success message
        return f"{to_read['title']} has been added to reading list"

    def get_to_read_list(self):
        to_read_list = db_utils.get_all_books(table='to_read_books')

        # Return reading list
        return to_read_list

    # function that takes in the book to be added to the to-read list and adds it to the table in the db.
    def add_to_read_list(self, read):
        # read should be a dictionary for the book from the user interaction
        # check if book already in the to_read list
        book_list = db_utils.get_all_books('read_books')
        titles_in_read_list = (book[0] for book in book_list)
        if read['title'] in titles_in_read_list:
            raise BookAlreadyOnTable('This book is already on the read list')
        # Call function to add book to list of books already read
        db_utils.insert_book(table='read_books', title=read['title'], author=read['author'],
                             category=read['categories'])

        # Return success message
        return f"{read['title']} has been added to books read list"

    # function that deletes a book from the to-read list. Put in the title that needs to be deleted and it will take
    # away that entry
    def delete_from_to_read_list(self, title):
        # check if book actually in to_read_list, if not raise error
        book_list = db_utils.get_all_books('to_read_books')
        titles_in_to_read_list = (book[0].lower() for book in book_list)
        if title.lower() not in titles_in_to_read_list:
            raise BookNotFound('This book is not in the to-read list')
        else:
            db_utils.delete_book(table='to_read_books', book_title=title)

    def delete_from_read_list(self, title):
        # check if book actually in to_read_list, if not raise error
        book_list = db_utils.get_all_books('read_books')
        titles_in_read_list = (book[0].lower() for book in book_list)
        if title.lower() not in titles_in_read_list:
            raise BookNotFound('This book is not in the read list')
        else:
            db_utils.delete_book(table='read_books', book_title=title)

    # function that brings the read_list from the db_utils file
    def get_read_list(self):
        # Call function to get list of books already read
        read_list = db_utils.get_all_books(table='read_books')

        # Return list of books already read
        return (read_list)

    # function that takes in the user review and the book you want to add the review too and adds the review to the stored table
    # if the book is not in the table an error is raised
    def add_a_review(self, read, user_review):
        # logic here for if the book is not in the list an error is raised
        book_list = db_utils.get_all_books('read_books')
        titles_in_to_read_list = (book[0] for book in book_list)
        if read['title'] not in titles_in_to_read_list:
            raise BookNotFound('Book not found on read_books list')
        # else user_review is added
        return db_utils.update_review(read['title'], user_review)

    # function that takes in a book in the book and adds a star rating to the book in the stored table
    def add_star_rating(self, read, user_rating):
        # logic here for if the book is not in the list an error is raised
        book_list = db_utils.get_all_books('read_books')
        titles_in_to_read_list = (book[0] for book in book_list)
        if read['title'] not in titles_in_to_read_list:
            raise BookNotFound('Book not found on read_books list')
        # else user_rating is added
        return db_utils.update_rating(read['title'], user_rating)

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


class InternalAPI:
    def __init__(self):
        self.book_app_api = BookAppAPI()

    # function to remove anything from the dictionary that is empty. Cleans up the user input
    def clean_user_input(self, user_input):
        return {k: v for k, v in user_input.items() if v != ''}

    # Endpoint to get 1-10 book suggestions after user inputs search
    # @app.route('/books/search', methods=['GET'])
    def search_book_suggestions(self, user_input):
        user_input = self.clean_user_input(user_input)
        # Call function to get a book suggestions
        book_suggestions = self.book_app_api.get_filtered_results(user_input)

        # check for duplicates from to_read_list
        book_suggestions = self.check_for_duplicates_from_to_read_list(user_input, book_suggestions)

        # check for duplicates from read_list
        book_suggestions = self.check_for_duplicates_from_read_list(user_input, book_suggestions)

        # Return book suggestion
        return {'Suggestions': book_suggestions}
        # print this in user interactions class

    # function to check where the books that have been searched for are already in the to_read_list. If they are,
    # those books are replaced by a new search. If it goes through 3 searches and still can't find new books, it
    # returns however many new books it can.
    def check_for_duplicates_from_to_read_list(self, user_input, book_suggestions):
        # Write code here to say if the suggestions are in the to_read_list, generate suggestions to replace
        book_list = db_utils.get_all_books('to_read_books')
        # a tuple of all the titles in the to_read_books list
        titles_in_to_read_list = (book[0] for book in book_list)
        # repeat_books is a tuple of book titles that have been suggested but are also in the to_read_books list
        repeat_books_to_remove = (book_suggestion['title'] for book_suggestion in book_suggestions if
                                  book_suggestion['title'] in titles_in_to_read_list)
        # removing book suggestions that are already on the to_read list
        book_suggestions = [book for book in book_suggestions if book['title'] not in repeat_books_to_remove]

        # how many more books are needed to satisfy the users request given some have been removed as repeats?
        number_to_replace = user_input['book_num'] - len(book_suggestions)

        if number_to_replace == 0:
            return book_suggestions  # No more replacements needed, return the suggestions

        count = 0
        while count < 3:
            # call the external API to generate number_to_replace new responses
            user_input['book_num'] = number_to_replace
            new_book_suggestions = self.book_app_api.get_filtered_results(user_input)

            if len(new_book_suggestions) == 0:
                return {f"For your given criteria, it's only possible to return {len(book_suggestions)} books.": book_suggestions}

            if len(book_suggestions) == 0:
                book_suggestions = new_book_suggestions

            # add the new_book_suggestions to the list of book_suggestions
            book_suggestions += new_book_suggestions

            count += 1

        if count == 3:
            return {f"For your given criteria, it's only possible to return {len(book_suggestions)} books.": book_suggestions}

        return book_suggestions

    # function to check whether the books that have been searched for are already in the read_list. If they are,
    # those books are replaced by a new search. If it goes through 3 searches and still can't find new books, it
    # returns however many new books it can.
    def check_for_duplicates_from_read_list(self, user_input, book_suggestions):
        # Write code here to say if the suggestions are in the to_read_list, generate suggestions to replace
        book_list = db_utils.get_all_books('read_books')
        # a tuple of all the titles in the to_read_books list
        titles_in_to_read_list = (book[0] for book in book_list)
        # repeat_books is a tuple of book titles that have been suggested but are also in the to_read_books list
        repeat_books_to_remove = (book_suggestion['title'] for book_suggestion in book_suggestions if
                                  book_suggestion['title'] in titles_in_to_read_list)
        # removing book suggestions that are already on the to_read list
        book_suggestions = [book for book in book_suggestions if book['title'] not in repeat_books_to_remove]

        # how many more books are needed to satisfy the users request given some have been removed as repeats?
        number_to_replace = user_input['book_num'] - len(book_suggestions)
        # call the external API to generate number_to_replace new responses
        if number_to_replace == 0:
            return book_suggestions  # No more replacements needed, return the suggestions

        count = 0
        while count < 3:

            user_input['book_num'] = number_to_replace
            new_book_suggestions = self.book_app_api.get_filtered_results(user_input)

            if len(new_book_suggestions) == 0:
                return {
                    f"For your given criteria, it's only possible to return {len(book_suggestions)} books.": book_suggestions}

            if len(book_suggestions) == 0:
                book_suggestions = new_book_suggestions

            # add the new_book_suggestions to the list of book_suggestions
            book_suggestions += new_book_suggestions

            count += 1

        if count == 3:
            return {
                f"For your given criteria, it's only possible to return {len(book_suggestions)} books.": book_suggestions}

        return book_suggestions

    # Endpoint to get 1 random book suggestion
    # @app.route('/books/random_suggestion', methods=['GET'])
    def random_book_suggestion(self, user_input):
        user_input = self.clean_user_input(user_input)
        random_book = self.book_app_api.get_random_result(user_input)

        # Write code here to say if the suggestion is in the already_read_list, randomly generate another suggestion

        # check for duplicates from to_read_list
        random_book = self.check_for_duplicates_from_to_read_list(user_input, random_book)

        # check for duplicates from read_list
        random_book = self.check_for_duplicates_from_read_list(user_input, random_book)

        # Return random_book
        return ({'Random Book': random_book})

    #
    #
    # Endpoint to add a book to the reading list
    # @app.route('/books/reading_list', methods=['POST'])
    def add_to_to_read_list(self, to_read):
        # to_read should be a dictionay coming from the user interactions where it gives the author, title, etc
        #check if book is already on the list. If it is an exception is raised
        book_list = db_utils.get_all_books('to_read_books')
        titles_in_to_read_list = (book[0] for book in book_list)
        if to_read['title'] in titles_in_to_read_list:
            raise BookAlreadyOnTable('This book is already on the to read list')

        # Call function to add book to reading list
        db_utils.insert_book(table='to_read_books', title=to_read['title'], author=to_read['author'],
                             category=to_read['category'])

        # Return success message
        return f"{to_read['title']} has been added to reading list"

    # Endpoint to get the to read list
    # @app.route('/books/reading_list', methods=['GET'])
    def get_to_read_list(self):
        to_read_list = db_utils.get_all_books(table='to_read_books')

        # Return reading list
        return to_read_list

    # Endpoint to add a book to the read list
    # @app.route('/books/already_read', methods=['POST'])
    def add_to_read_list(self, read):
        # read should be a dictionary for the book from the user interaction
        # check if book already in the to_read list
        book_list = db_utils.get_all_books('read_books')
        titles_in_read_list = (book[0] for book in book_list)
        if read['title'] in titles_in_read_list:
            raise BookAlreadyOnTable('This book is already on the read list')
        # Call function to add book to list of books already read
        db_utils.insert_book(table='read_books', title=read['title'], author=read['author'],
                             category=read['category'])

        # Return success message
        return f"{read['title']} has been added to books read list"

        # Endpoint to get the read books list
        # @app.route('/books/read', methods=['GET'])

    def get_read_list(self):
        # Call function to get list of books already read
        read_list = db_utils.get_all_books(table='read_books')

        # Return list of books already read
        return (read_list)

    def add_a_review(self, read, user_review):
        # logic here for if the book is not in the list an error is raised
        book_list = db_utils.get_all_books('read_books')
        titles_in_to_read_list = (book[0] for book in book_list)
        if read['title'] not in titles_in_to_read_list:
            raise BookNotFound('Book not found on read_books list')
        #else user_review is added
        return db_utils.update_review(read['title'], user_review)

    def add_star_rating(self, read, user_rating):
        # logic here for if the book is not in the list an error is raised
        book_list = db_utils.get_all_books('read_books')
        titles_in_to_read_list = (book[0] for book in book_list)
        if read['title'] not in titles_in_to_read_list:
            raise BookNotFound('Book not found on read_books list')
        #else user_rating is added
        return db_utils.update_rating(read['title'], user_rating)


internal_api = InternalAPI()
print(internal_api.check_for_duplicates_from_to_read_list(user_input={'book_num': 1, 'book_type': 'fiction'},
                                                          book_suggestions=[
                                                              {'title': 'The B.F.G', 'authors': 'Rhoal Dahl'}]))

# internal_api = InternalAPI()
# to_read_list = internal_api.get_to_read_list()
# read_list = internal_api.get_read_list()

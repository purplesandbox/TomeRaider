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
        # Write code here to say if the suggestions are in the already_read_list, generate another set of suggestions
        # for suggestion in book_suggestions:
        #list of book titles in table
        count = 0
        for book_suggestion in book_suggestions['title']:
            for titles in db_utils.get_all_books('read_books')[0]:
                if book_suggestion == titles:
                    count += 1
                    indx = book_suggestions.index(book_suggestion)
                    book_suggestions.remove(indx)
#put titles for read books into a set
        #filter out of book suggestions if title in set

        # Return book suggestion
        return {'Suggestions': book_suggestions}
        # print this in user interactions class

    # Endpoint to get 1 random book suggestion
    # @app.route('/books/random_suggestion', methods=['GET'])
    def random_book_suggestion(self, user_input):
        user_input = self.clean_user_input(user_input)
        random_book = self.book_app_api.get_random_result(user_input)

        # Write code here to say if the suggestion is in the already_read_list, randomly generate another suggestion

        # Return book suggestion
        return ({'Random Book': random_book})

    #
    #
    # Endpoint to add a book to the reading list
    # @app.route('/books/reading_list', methods=['POST'])
    def add_to_to_read_list(self, to_read):
        # to_read should be a dictionay coming from the user interactions where it gives the author, title, etc

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
        # logic here for if the book is not in the list
        return db_utils.update_review(read['title'], user_review)

    def add_star_rating(self, read, user_rating):
        # logic here for if the book is not in the list
        return db_utils.update_rating(read['title'], user_rating)


#
#

internal_api = InternalAPI()
to_read_list = internal_api.get_to_read_list()
read_list = internal_api.get_read_list()

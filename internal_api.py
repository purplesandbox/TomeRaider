from flask import Flask, jsonify
from API_results import BookFinderAPICalls
from pprint import pp

app = Flask(__name__)

# Note: For category, the user has to input each word starting with a capital letter. The API will return an error
# as it is case-sensitive

class BookAppAPI:
    def __init__(self):
        self.book_finder_api = BookFinderAPICalls()

    #function to remove anything from the dictionary that is empty. Cleans up the user input
    def clean_user_input(self, user_input):
        return {k:v for k,v in user_input.items() if v != ''}


    # Endpoint to get 1-10 book suggestions after user inputs search
    @app.route('/books/search', methods=['GET'])
    def search_book_suggestions(self, user_input):
        user_input = self.clean_user_input(user_input)
        # Call function to get a book suggestions
        book_suggestions = self.book_finder_api.get_filtered_results(user_input)
        # Write code here to say if the suggestions are in the already_read_list, generate another set of suggestions
        # for suggestion in book_suggestions:
        #     if suggestion == "xxx": #need to write code to get list of books in database
        #         book_suggestions = BookFinderAPICalls.get_filtered_results(user_input) #check this
        # Return book suggestion
        return {'Suggestions': book_suggestions}
        #print this in user interactions class

    # Endpoint to get 1 random book suggestion
    @app.route('/books/random_suggestion', methods=['GET'])
    def random_book_suggestion(self, user_input):
        user_input = self.clean_user_input(user_input)
        random_book = self.book_finder_api.get_random_result(user_input)

        # Write code here to say if the suggestion is in the already_read_list, randomly generate another suggestion

        # Return book suggestion
        return ({'Random Book': random_book})
#
#
# # Endpoint to add a book to the reading list
# @app.route('/books/reading_list', methods=['POST'])
# def add_to_reading_list(book_title):
#
#
#     # Call function to add book to reading list
#     add_book_to_to_read_list(book_title)
#
#     # Return success message
#     return ({'message': 'Book added to reading list'})
#
#
# # Endpoint to add a book to the list of books already read
# @app.route('/books/already_read', methods=['POST'])
# def add_to_read_list(book_title):
#
#     # Call function to add book to list of books already read
#     add_book_to_read_list(book_title)
#
#     # Return success message
#     return ({'message': 'Book added to list of books already read'})
#
#
# # Endpoint to get the reading list
# @app.route('/books/reading_list', methods=['GET'])
# def get_to_read_list():
#     # Call function to get reading list
#     reading_list = get_reading_list()
#
#     # Return reading list
#     return ({'reading_list': reading_list})
#
#
# # Endpoint to get the list of books already read
# @app.route('/books/read', methods=['GET'])
# def get_read_list():
#     # Call function to get list of books already read
#     read_list = get_read_list()
#
#     # Return list of books already read
#     return ({'already_read_list': read_list})
#
#


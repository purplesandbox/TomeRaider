from flask import Flask, jsonify
from API_results import BookFinderAPICalls
from pprint import pp

app = Flask(__name__)

class BookAppAPI:
    def __init__(self):
        self.book_finder_api = BookFinderAPICalls()

    # Endpoint to get 1-10 book suggestions after user inputs search
    @app.route('/books/search', methods=['GET'])
    def search_book_suggestions(self, user_input):
        book_suggestions = self.book_finder_api.get_filtered_results(user_input)
        # Write code here to say if the suggestions are in the already_read_list, generate another set of suggestions
        # for suggestion in book_suggestions:
        #     if suggestion == "xxx": #need to write code to get list of books in database
        #         book_suggestions = BookFinderAPICalls.get_filtered_results(user_input) #check this
        # Return book suggestion
        return {'Suggestions': book_suggestions}
        #print this in user interactions class
#
# # Endpoint to get 1 book suggestions
# @app.route('/books/random_suggestion', methods=['POST'])
# def random_book_suggestion(book_type, category):
#     # Get user inputs for criteria for the book from the user inputs
#
#     # Call function to get a book suggestion
#     book_suggestion = InterfacesWithExternalAPI.book_filtering_function(category, book_type, number_of_books=1)
#     # Write code here to say if the suggestion is in the already_read_list, randomly generate another suggestion
#
#     # Return book suggestion
#     return jsonify({'book': book_suggestion})
#
#
# # Endpoint to add a book to the reading list
# @app.route('/books/reading_list', methods=['POST'])
# def add_to_reading_list(book_title):
#     # Get user input
#
#     # Call function to add book to reading list
#     add_book_to_reading_list(book_title)
#
#     # Return success message
#     return jsonify({'message': 'Book added to reading list'})
#
#
# # Endpoint to add a book to the list of books already read
# @app.route('/books/already_read', methods=['POST'])
# def add_to_already_read_list(book_title):
#     # Get user input
#
#     # Call function to add book to list of books already read
#     add_book_to_already_read_list(book_title)
#
#     # Return success message
#     return jsonify({'message': 'Book added to list of books already read'})
#
#
# # Endpoint to get the reading list
# @app.route('/books/reading_list', methods=['GET'])
# def get_reading_list():
#     # Call function to get reading list
#     reading_list = get_reading_list()
#
#     # Return reading list
#     return jsonify({'reading_list': reading_list})
#
#
# # Endpoint to get the list of books already read
# @app.route('/books/read', methods=['GET'])
# def get_read_list():
#     # Call function to get list of books already read
#     read_list = get_read_list()
#
#     # Return list of books already read
#     return jsonify({'already_read_list': read_list})
#
#


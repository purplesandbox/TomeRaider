import db_utils
from internal_api import InternalAPI, BookNotFound, BookAlreadyOnTable
from pprint import pprint as pp
from tabulate import tabulate

class UserInteractions:
    def __init__(self):
        self.book_criteria = {
            'author': '',
            'categories': '',
            'book_type': '',
            'lexile_min': '',
            'lexile_max': '',
            'book_num': '',
            'random_choice': False,
            'filtered_choice': False
        }
        self.genre_choices = {
            '1': 'Animals, Bugs & Pets',
            '2': 'Art, Creativity & Music',
            '3': 'General Literature',
            '4': 'Hobbies, Sports & Outdoors',
            '5': 'Science Fiction & Fantasy',
            '6': 'Real Life',
            '7': 'Science & Technology',
            '8': 'Mystery & Suspense',
            '9': 'Reference'
        }
        self.internal_api = InternalAPI()

        self.read_book_dict = {
            'title': '',
            'author': '',
            'categories': ''
        }

    """Welcome function which contains the options for user to select, directs user to the relevant function"""

    # Tests written
    def welcome(self):
        while True:
            user_choice = input("""Welcome to TomeRaider!\nWhat would you like to do?
            If you would like to search for a book, enter 'search'.
            If you would like to generate a random book, enter 'random'.
            If you would like to look at your to-read list, enter 'to-read'.
            If you would like to look at your read list, enter 'read'.
            If you would like to add a book to your read list, enter 'add'.
            If you would like to delete a book from a list, enter 'delete'.
            Enter 'exit' to exit the program.\nPlease enter: """)
            lowercase_choice = user_choice.lower()

            if lowercase_choice == 'search':
                self.filtered_choice()
            elif lowercase_choice == 'random':
                self.random_choice()
            elif lowercase_choice == 'to-read':
                self.view_to_read_list()
            elif lowercase_choice == 'read':
                self.view_read_list()
            elif lowercase_choice == 'exit':
                print('Goodbye!')
                break
            elif lowercase_choice == 'add':
                self.add_book_to_read_list()
            elif lowercase_choice == 'delete':
                self.delete_book()
            else:
                print('Invalid choice. Please try again.')

    """function to ask user to enter the number of books they want to return
        this continues to loop until a valid response is given"""

    # Tests written
    def get_number_of_books(self):
        while True:
            try:
                number_of_books = int(
                    input('How many books would you like to search for? (Enter a number between 1 and 10): '))
                if number_of_books < 1 or number_of_books > 10:
                    print('Invalid input. Please enter a number between 1 and 10.')
                else:
                    return number_of_books
            except ValueError:
                print('Invalid input. Please try again.')

    """function to return the search criteria messages for filtered_choice book(s)"""

    # Tests written
    def print_search_criteria_message(self):
        print('What would you like to search by? (Press enter if you would like to leave blank):')

    """function to display the genres available to user """

    # Tests written
    def print_book_genre_dictionary(self):
        print('You can choose from the following categories:')
        for key, value in self.genre_choices.items():
            print(f"{key}: {value}")

    """ function to validate the user's genre choice """

    # SOME tests written
    def get_valid_genre_choice(self):

        while True:
            genre_input = input(
                'Please enter the number that corresponds with your genre choice. (Press enter if you do not have a preference)')
            if genre_input == '':
                return None
            elif genre_input in self.genre_choices.keys():
                return self.genre_choices[genre_input]
            else:
                print('Invalid genre choice. Please choose a valid number from the genre choices.')

    """ function to validate the user's yes or no input """

    # SOME tests written

    def validate_input_y_or_n(self, prompt):
        while True:
            user_input = input(prompt)
            if user_input.lower() == 'y' or user_input.lower() == 'n':
                return user_input.lower()
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    """ function to allow user to search for a book and input different search params """

    # Not started tests yet, looks tricky....
    def filtered_choice(self):
        number_of_books = self.get_number_of_books()
        self.book_criteria['book_num'] = number_of_books
        self.book_criteria['filtered_choice'] = True

        self.print_search_criteria_message()
        author_input = input('Author: ')

        self.print_book_genre_dictionary()
        genre_input = self.get_valid_genre_choice()

        fiction_input = input('Fiction or NonFiction: ')
        lexile_min_input = input('Lexile min: ')
        lexile_max_input = input('Lexile max: ')

        self.book_criteria['author'] = author_input
        self.book_criteria['categories'] = genre_input
        self.book_criteria['book_type'] = fiction_input
        self.book_criteria['lexile_min'] = lexile_min_input
        self.book_criteria['lexile_max'] = lexile_max_input

        self.filtered_books = self.internal_api.search_book_suggestions(user_input=self.book_criteria)
        for index, element in enumerate(self.filtered_books):
            print(f"{index + 1})")
            pp(element)
        self.add_filtered_book_to_to_read_list()

    """Function which allows user to choose a book genre to generate a random book"""

    def random_choice(self):
        self.print_book_genre_dictionary()
        chosen_genre = self.get_valid_genre_choice()

        self.book_criteria['categories'] = chosen_genre
        self.book_criteria['random_choice'] = True

        random_book = self.internal_api.random_book_suggestion(user_input=self.book_criteria)
        pp(random_book)
        self.add_random_book_to_to_read_list(random_book)

    """ function to add random book to to read list """

    def add_random_book_to_to_read_list(self, random_book):
        add_or_not = self.validate_input_y_or_n('Would you like you add to your to-read list? (y/n)')
        if add_or_not == 'y':
            self.internal_api.add_to_to_read_list(random_book)
        else:
            print("Nothing has been added to your to-read list.")

    """ function to add filtered book to to read list """

    def add_filtered_book_to_to_read_list(self):
        add_or_not = self.validate_input_y_or_n('Would you like to add a book to your to-read list? (y/n) ')
        while add_or_not == 'y':
            self.book_to_add_from_the_sequence = self.get_book_details_from_the_sequence_number()
            self.internal_api.add_to_to_read_list(self.book_to_add_from_the_sequence)
            add_another_book = self.validate_input_y_or_n(
                "Would you like to add another book to your to-read list? (y/n) ")
            if add_another_book == 'n':
                print("Nothing has been added to your to-read list.")
                break
            else:
                add_or_not == 'y'


        if add_or_not == 'n':
            print("Nothing has been added to your to-read list.")

    """ function to ask for book details that user would like to add to read list """

    # Tests for all details, no author and no title. No genre doesn't work
    def get_book_details(self):
        self.book_to_add = {
            'authors': input("Please enter the author(s) of the book: "),
            'title': input("Please enter the title of the book: ")
        }
        self.print_book_genre_dictionary()
        self.book_to_add['categories'] = self.get_valid_genre_choice()
        return self.book_to_add

    """ function to prompt the user to select the book from the filtered selection to collect the book details"""

    def get_book_details_from_the_sequence_number(self):
            self.book_to_add_from_the_sequence_validated = self.get_valid_filtered_book_choice()
            del self.book_to_add_from_the_sequence_validated['summary']
            author = self.book_to_add_from_the_sequence_validated['authors']
            self.book_to_add_from_the_sequence_validated['authors'] = author[0]
            category = self.book_to_add_from_the_sequence_validated['categories']
            self.book_to_add_from_the_sequence_validated['categories'] = category[0]
            return self.book_to_add_from_the_sequence_validated



    """function to validate entry of filtered books"""

    def get_valid_filtered_book_choice(self):

        while True:
            self.book_from_the_filtered_list = input("""Please enter the number that corresponds to the book you would like to add:""")
            if self.book_from_the_filtered_list.isdigit():
                self.book_from_the_filtered_list = int(self.book_from_the_filtered_list) - 1
                if self.book_from_the_filtered_list >= 0 and self.book_from_the_filtered_list <= len(self.filtered_books):
                    self.book_to_add_from_the_sequence = self.filtered_books[self.book_from_the_filtered_list]
                    if 'summary' in self.book_to_add_from_the_sequence.keys():
                        return self.book_to_add_from_the_sequence
                    else:
                        print("This book has been already selected!")
                        self.get_book_details_from_the_sequence_number()

                else:
                    print("The sequence number entered is out of the provided book range. Please, try again!")
                    self.add_filtered_book_to_to_read_list()
            elif self.book_from_the_filtered_list == '' or isinstance(self.book_from_the_filtered_list, str):
                print("Please enter the NUMBER that corresponds to the book you would like to add to your to-read list!")
                self.add_filtered_book_to_to_read_list()




    """ function to add book to read list """
    def add_book_to_read_list(self):
        while True:
            book_to_add = self.get_book_details()
            self.read_book_dict['title'] = book_to_add['title']
            self.read_book_dict['author'] = book_to_add['authors']
            self.read_book_dict['categories'] = book_to_add['categories']

            try:
                self.internal_api.add_to_read_list(self.read_book_dict)
                break
            except BookAlreadyOnTable:
                print("This book is already on the to-read list! Please try again.")
            finally:
                self.user_review_and_call_star_rating(read=self.read_book_dict)

    """ function to ask user whether they would like to add a star rating """

    def star_rating(self, read):
        while True:
            add_star_rating = input('Would you like to add a star rating for the book? (y/n) ')
            if add_star_rating == 'y':
                user_rating = self.get_valid_star_rating()
                self.internal_api.add_star_rating(read, user_rating)
                break
            elif add_star_rating == 'n':
                print("No star rating has been added.")
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'")

    """ function to validate the user star rating input """

    def get_valid_star_rating(self):
        while True:
            rating = input('How many stars would you like to rate this book? (Enter a number between 1 and 5): ')
            try:
                user_rating = int(rating)
                if 1 <= user_rating <= 5:
                    return user_rating
                else:
                    print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Please enter a valid number.")

    """ function to ask if user would like to add a review and then ask if they want to add a star rating """

    def user_review_and_call_star_rating(self, read):
        while True:
            review = input('Would you like to add a review for this book? (y/n) ')
            if review == 'y':
                book_review = input('Add your review: ')
                self.internal_api.add_a_review(read, book_review)
                self.star_rating(read)
                break
            elif review == 'n':
                self.star_rating(read)
                break

    """ function to view to read list """

    def view_to_read_list(self):
        to_read_list = self.internal_api.get_to_read_list()

        if not to_read_list:
            return "Your To-Read list is empty."
        else:
            headers = ['Title', 'Author', 'Category']
            print(tabulate(to_read_list, headers, tablefmt='grid'))

    """ function to ask user which list they want to delete a book from """

    def delete_book(self):
        while True:
            which_list = input("Which list would you like to delete a book from? ('to-read' or 'read')")
            if which_list.lower() == 'to-read':
                self.delete_from_to_read_list()
                break
            elif which_list.lower() == 'read':
                self.delete_from_read_list()
                break
            else:
                print("Invalid choice. Please try again.")

    """ function to ask user which book they want to delete from read list """

    def delete_from_read_list(self):
        while True:
            book_to_delete = input(
                "Please enter the title of the book you would like to delete (or enter 'cancel' to go back): ")
            lower_case_book_to_delete = book_to_delete.lower()
            if lower_case_book_to_delete == 'cancel':
                print("Deletion cancelled.")
                break
            try:
                self.internal_api.delete_from_read_list(lower_case_book_to_delete)
                print(f"{book_to_delete} has been deleted.")
                break
            except BookNotFound:
                print(f"{book_to_delete} is not in your to-read list. Please try again.")

    """ function to ask user which book they would like to delete from to-read list """

    def delete_from_to_read_list(self):
        while True:
            book_to_delete = input(
                "Please enter the title of the book you would like to delete (or enter 'cancel' to go back): ")
            lower_case_book_to_delete = book_to_delete.lower()
            if lower_case_book_to_delete == 'cancel':
                print("Deletion cancelled.")
                break
            try:
                self.internal_api.delete_from_to_read_list(lower_case_book_to_delete)
                print(f"{book_to_delete} has been deleted.")
                break
            except BookNotFound:
                print(f"{book_to_delete} is not in your to-read list. Please try again.")


user1 = UserInteractions()
user1.welcome()

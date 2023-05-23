import db_utils
from internal_api import InternalAPI, BookNotFound, BookAlreadyOnTable
from pprint import pp
from tabulate import tabulate

"""User interactions class containing internal API, and default values for book criteria"""


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
        self.internal_api = InternalAPI()

        self.read_book_dict = {
            'title': '',
            'author': '',
            'categories': ''
        }

    """Welcome function which contains the options for user to select, directs user to the relevant function"""

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

    def print_search_criteria_message(self):
        print('What would you like to search by? (Press enter if you would like to leave blank):')

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

        filtered_books = self.internal_api.search_book_suggestions(user_input=self.book_criteria)
        pp(filtered_books)
        self.add_filtered_book_to_to_read_list(filtered_books)

    """function to display genre choices to user"""

    def print_book_genre_dictionary(self):
        genre_choices = {
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
        print('You can choose from the following categories:')
        for key, value in genre_choices.items():
            print(f"{key}: {value}")

    def get_valid_genre_choice(self):
        genre_choices = {
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
        while True:
            genre_input = input(
                'Please enter the number that corresponds with your genre choice. (Press enter if you do not have a preference)')
            if genre_input == '':
                return None
            elif genre_input in genre_choices.keys():
                return genre_choices[genre_input]
            else:
                print('Invalid genre choice. Please choose a valid number from the genre choices.')

    """Function which allows user to choose a book genre to generate a random book"""

    def random_choice(self):
        self.print_book_genre_dictionary()
        chosen_genre = self.get_valid_genre_choice()

        self.book_criteria['categories'] = chosen_genre
        self.book_criteria['random_choice'] = True

        random_book = self.internal_api.random_book_suggestion(user_input=self.book_criteria)
        pp(random_book)
        self.add_random_book_to_to_read_list(random_book)

    def add_random_book_to_to_read_list(self, random_book):
        add_or_not = self.validate_input_y_or_n('Would you like you add to your to-read list? (y/n)')
        if add_or_not == 'y':
            self.internal_api.add_to_to_read_list(random_book)
        else:
            print("Nothing has been added to your to-read list.")

    def validate_input_y_or_n(self, prompt):
        while True:
            user_input = input(prompt)
            if user_input.lower() == 'y' or user_input.lower() == 'n':
                return user_input.lower()
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    def add_filtered_book_to_to_read_list(self, filtered_book):
        add_or_not = self.validate_input_y_or_n('Would you like to add a book to your to-read list? (y/n) ')
        while add_or_not == 'y':
            book_to_add = self.get_book_details()
            self.internal_api.add_to_to_read_list(book_to_add)

            add_another_book = self.validate_input_y_or_n(
                "Would you like to add another book to your to-read list? (y/n) ")
            if add_another_book == 'n':
                print("Nothing has been added to your to-read list.")
                break

        if add_or_not == 'n':
            print("Nothing has been added to your to-read list.")

    def get_book_details(self):
        book_to_add = {
            'authors': input("Please enter the author(s) of the book: "),
            'title': input("Please enter the title of the book: ")
        }
        self.print_book_genre_dictionary()
        book_to_add['categories'] = self.get_valid_genre_choice()
        return book_to_add

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

    def view_to_read_list(self):
        to_read_list = self.internal_api.get_to_read_list()

        if not to_read_list:
            return "Your To-Read list is empty."
        else:
            headers = ['Title', 'Author', 'Category']
            print(tabulate(to_read_list, headers, tablefmt='grid'))

    def view_read_list(self):
        read_list = self.internal_api.get_read_list()

        if not read_list:
            return "Your Read list is empty."
        else:
            headers = ['Title', 'Author', 'Category', 'Review', 'Star Rating']
            print(tabulate(read_list, headers, tablefmt='grid'))

    def regenerate_results(self):
        while True:
            happy_with_results = input('Would you like to generate different books? (y/n)')
            if happy_with_results.lower() == 'y':
                return True
            elif happy_with_results.lower() == 'n':
                return False
            else:
                print('Invalid choice. Please try again.')


#
#


user1 = UserInteractions()
user1.welcome()
# user2 = UserInteractions()
# user2.view_read_list()

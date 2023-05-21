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
            'random_choice': False,   def welcome(self):
        while True:
            user_choice = input("""Welcome to {APP NAME}!\nWhat would you like to do?
            If you would like to search for a book, enter 'search'.
            If you would like to generate a random book, enter 'random'.
            If you would like to look at your to-read list, enter 'to-read'.
            If you would like to look at your read list, enter 'read'.
            To exit the program, enter 'exit'.\nPlease enter: """)
            lowercase_choice = user_choice.lower()
            if lowercase_choice == 'search':
                self.filtered_choice()
                break
            elif lowercase_choice == 'random':
                self.random_choice()
                break
            elif lowercase_choice == 'to-read':
                self.view_to_read_list()
                break
            elif lowercase_choice == 'read':
                self.view_read_list()
                break
            elif lowercase_choice == 'exit':
                print('Goodbye!')
                break
            else:
                print('Invalid choice. Please try again.')
            'filtered_choice': False
        }
        self.internal_api = InternalAPI()

"""Welcome function which contains the options for user to select, directs user to the relevant function"""
    def welcome(self):
        while True:
            user_choice = input("""Welcome to {APP NAME}!\nWhat would you like to do?
            If you would like to search for a book, enter 'search'.
            If you would like to generate a random book, enter 'random'.
            If you would like to look at your to-read list, enter 'to-read'.
            If you would like to look at your read list, enter 'read'.
            To exit the program, enter 'exit'.\nPlease enter: """)
            lowercase_choice = user_choice.lower()
            if lowercase_choice == 'search':
                self.filtered_choice()
                break
            elif lowercase_choice == 'random':
                self.random_choice()
                break
            elif lowercase_choice == 'to-read':
                self.view_to_read_list()
                break
            elif lowercase_choice == 'read':
                self.view_read_list()
                break
            elif lowercase_choice == 'exit':
                print('Goodbye!')
                break
            else:
                print('Invalid choice. Please try again.')

"""Function which allows user to input book selection criteria and calls API"""
    def filtered_choice(self):
        while True:
            try:
                number_of_books = int(
                    input('How many books would you like to search for? (Enter a number between 1 and 10) '))
                if number_of_books < 1 or number_of_books > 10:
                    raise ValueError('Invalid input. Please enter a number between 1 and 10.')
                break
            except ValueError as e:
                print(str(e))
                continue

        self.book_criteria['book_num'] = number_of_books
        self.book_criteria['filtered_choice'] = True

        print('What would you like to search by? (Press enter if you would like to leave blank):')
        author = input('Author: ')
        genre = input('Genre: ')
        fiction = input('Fiction or Non-Fiction: ')
        lexile_min = input('Lexile min: ')
        lexile_max = input('Lexile max: ')

        self.book_criteria['author'] = author
        self.book_criteria['categories'] = genre
        self.book_criteria['book_type'] = fiction
        self.book_criteria['lexile_min'] = lexile_min
        self.book_criteria['lexile_max'] = lexile_max

        pp(self.internal_api.search_book_suggestions(user_input=self.book_criteria))

"""Function which allows user to choose a book genre to generate a random book"""
    def random_choice(self):
        chosen_genre = input('What genre are you looking for? ')

        self.book_criteria['categories'] = chosen_genre
        self.book_criteria['random_choice'] = True

        pp(self.internal_api.random_book_suggestion(user_input=self.book_criteria))

    def add_book_to_list_or_not(self):
        while True:
            add_to_list_or_not = input('Would you like to add this book to a list? (y/n): ')
            if add_to_list_or_not.lower() == 'y':
                return True
            elif add_to_list_or_not.lower() == 'n':
                return False
            else:
                print('Invalid choice. Please try again.')

    def add_star_rating(self, read):
        book_list = db_utils.get_all_books('read_books')
        titles_in_to_read_list = [book['title'] for book in book_list]

        if read['title'] not in titles_in_to_read_list:
            raise BookNotFound('Book not found on read_books list')

        user_rating = self.star_rating()
        db_utils.update_rating(read['title'], user_rating)
        return user_rating

    def star_rating(self):
        while True:
            user_rating = input('How many stars would you like to rate this book? (Enter a number between 1 and 5): ')
            try:
                rating = int(user_rating)
                if 1 <= rating <= 5:
                    return rating
                else:
                    print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Please enter a valid number.")

    def add_a_review(self, read):
        book_list = db_utils.get_all_books('read_books')
        titles_in_to_read_list = [book['title'] for book in book_list]

        if read['title'] not in titles_in_to_read_list:
            raise BookNotFound('Book not found on read_books list')

        user_review = self.user_review()
        db_utils.update_review(read['title'], user_review)
        return user_review

    def user_review(self):
        user_review = input('Please enter your review for this book: ')
        return user_review

    def view_to_read_list(self):
        to_read_list = db_utils.get_all_books(table='to_read_books')

        if not to_read_list:
            return "Your to-read list is empty."
        else:
            table = []
            for book in to_read_list:
                table.append([book['title'], book['author'], book['category']])

            headers = ['Title', 'Author', 'Category']
            return tabulate(table, headers, tablefmt='grid')

    def view_read_list(self):
        read_list = db_utils.get_all_books(table='read_books')

        if not read_list:
            return "Your Read list is empty."
        else:
            table = []
            for book in read_list:
                table.append([book['title'], book['author'], book['category']])

            headers = ['Title', 'Author', 'Category', 'Review', 'Star Rating']
            return tabulate(table, headers, tablefmt='grid')

    def regenerate_results(self):
        while True:
            happy_with_results = input('Would you like to generate different books? (y/n)')
            if happy_with_results.lower() == 'y':
                return True
            elif happy_with_results.lower() == 'n':
                return False
            else:
                print('Invalid choice. Please try again.')


user1 = UserInteractions()
user1.welcome()

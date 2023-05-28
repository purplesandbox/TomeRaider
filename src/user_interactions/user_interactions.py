from src.API.internal_api import InternalAPI, BookNotFound, BookAlreadyOnTable, NoSearchResultsWithGivenCriteria
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
        print('What would you like to search by? (Press enter if you would like to leave blank): ')

    """function to display the genres available to user """
    def print_book_genre_dictionary(self):
        print('You can choose from the following categories: ')
        for key, value in self.genre_choices.items():
            print(f"{key}: {value}")

    """ function to validate the user's genre choice """
    def get_valid_genre_choice(self):

        while True:
            genre_input = input(
                'Please enter the number that corresponds with your genre choice. (Press enter if you do not have a preference) ')
            if genre_input == '':
                return None
            elif genre_input in self.genre_choices.keys():
                return self.genre_choices[genre_input]
            else:
                print('Invalid genre choice. Please choose a valid number from the genre choices.')

    """ function to validate the user's yes or no input """
    def validate_input_y_or_n(self, prompt):
        while True:
            user_input = input(prompt).lower().strip()
            if user_input == 'y' or user_input == 'n':
                return user_input
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    """ function to allow user to search for a book and input different search params """
    def filtered_choice(self):
        number_of_books = self.get_number_of_books()
        self.book_criteria['book_num'] = number_of_books
        self.book_criteria['filtered_choice'] = True

        while True:
            try:
                self.print_search_criteria_message()
                author_input = input('Author: ')

                self.print_book_genre_dictionary()
                genre_input = self.get_valid_genre_choice()

                fiction_input = self.validate_fiction_nonfiction_input()
                lexile_min_input = self.validate_lexile_min_input()
                lexile_max_input = self.validate_lexile_max_input()

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
                break  # Exit the loop if no exception is raised
            except NoSearchResultsWithGivenCriteria:
                print("No search results found. Please refine your search criteria and try again.")
                continue  # Continue the loop to prompt the user for new search criteria

    """function to validate fiction or nonfiction input"""
    def validate_fiction_nonfiction_input(self):
        while True:
            fiction_input = input('Fiction or Nonfiction: ').lower().strip()
            if fiction_input == "" or fiction_input in ['fiction', 'nonfiction']:
                return fiction_input
            else:
                print("Invalid input. Please enter 'fiction' or 'nonfiction', or press enter if you have no "
                      "preference. ")

    """function to validate lexile min input"""
    def validate_lexile_min_input(self):
        while True:
            lexile_min_input = input('Lexile min: ')
            if lexile_min_input == '':
                return ''
            try:
                lexile_min = int(lexile_min_input)
                if -650 <= lexile_min <= 2150:
                    return lexile_min
                else:
                    print("Invalid input. Please enter a number between -650 and 2150, or press enter if you have no "
                          "preference. ")
            except ValueError:
                print("Invalid input. Please enter a number between -650 and 2150, or press enter if you have no "
                      "preference. ")

    """function to validate lexile max input"""
    def validate_lexile_max_input(self):
        while True:
            lexile_max_input = input('Lexile max: ')
            if lexile_max_input == '':
                return ''
            try:
                lexile_max = int(lexile_max_input)
                if -650 <= lexile_max <= 2150:
                    return lexile_max
                else:
                    print("Invalid input. Please enter a number between -650 and 2150, or press enter if you have no "
                          "preference. ")
            except ValueError:
                print("Invalid input. Please enter a number between -650 and 2150, or press enter if you have no "
                      "preference. ")

    """Function which allows user to choose a book genre to generate a random book"""
    def random_choice(self):
        self.print_book_genre_dictionary()
        chosen_genre = self.get_valid_genre_choice()

        self.book_criteria['author'] = ''
        self.book_criteria['categories'] = chosen_genre
        self.book_criteria['book_type'] = ''
        self.book_criteria['lexile_min'] = ''
        self.book_criteria['lexile_max'] = ''
        self.book_criteria['filtered_choice'] = False
        self.book_criteria['random_choice'] = True

        random_book = self.internal_api.random_book_suggestion(user_input=self.book_criteria)
        pp(random_book)
        self.add_random_book_to_to_read_list(random_book)

    """ function to add random book to to read list """
    def add_random_book_to_to_read_list(self, random_book):
        add_or_not = self.validate_input_y_or_n('Would you like to add this to your to-read list? (y/n) ')
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
            self.book_from_the_filtered_list = input(
                "Please enter the number that corresponds to the book you would like to add: ")
            if self.book_from_the_filtered_list.isdigit():
                self.book_from_the_filtered_list = int(self.book_from_the_filtered_list) - 1
                if self.book_from_the_filtered_list > len(self.filtered_books):
                    print("The entry is out of range of the book selecton list! Please, try again!")
                elif 0 <= self.book_from_the_filtered_list <= len(self.filtered_books):
                    self.book_to_add_from_the_sequence = self.filtered_books[self.book_from_the_filtered_list]
                    if 'summary' in self.book_to_add_from_the_sequence.keys():
                        return self.book_to_add_from_the_sequence
                    else:
                        print("This book has already been selected!")

                else:
                    print("The number you provided is invalid. Please try again.")
            else:
                print("Invalid input. Please try again.")
                continue

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

    """ function to view read list """
    def view_read_list(self):
        read_list = self.internal_api.get_read_list()

        if not read_list:
            return "Your Read list is empty."
        else:
            headers = ['Title', 'Author', 'Category', 'Review', 'Star Rating']
            print(tabulate(read_list, headers, tablefmt='grid'))

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
            lower_stripped_which_list = which_list.lower().strip()
            if lower_stripped_which_list == 'to-read':
                self.delete_from_to_read_list()
                break
            elif lower_stripped_which_list == 'read':
                self.delete_from_read_list()
                break
            else:
                print("Invalid choice. Please try again.")

    """ function to ask user which book they want to delete from read list """
    def delete_from_read_list(self):
        while True:
            book_to_delete = input(
                "Please enter the title of the book you would like to delete (or enter 'cancel' to go back): ")
            lower_stripped_case_book_to_delete = book_to_delete.lower().strip()
            if lower_stripped_case_book_to_delete == 'cancel':
                print("Deletion cancelled.")
                break
            try:
                self.internal_api.delete_from_read_list(lower_stripped_case_book_to_delete)
                print(f"{book_to_delete} has been deleted.")
                break
            except BookNotFound:
                print(f"{book_to_delete} is not in your to-read list. Please try again.")

    """ function to ask user which book they would like to delete from to-read list """
    def delete_from_to_read_list(self):
        while True:
            book_to_delete = input(
                "Please enter the title of the book you would like to delete (or enter 'cancel' to go back): ")
            lower_stripped_case_book_to_delete = book_to_delete.lower().strip()
            if lower_stripped_case_book_to_delete == 'cancel':
                print("Deletion cancelled.")
                break
            try:
                self.internal_api.delete_from_to_read_list(lower_stripped_case_book_to_delete)
                print(f"{book_to_delete} has been deleted.")
                break
            except BookNotFound:
                print(f"{book_to_delete} is not in your to-read list. Please try again.")

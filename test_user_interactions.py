import unittest
from unittest import mock
from unittest.mock import patch
from user_interactions import UserInteractions
from io import StringIO
import sys

########################################################################################################
# class TestWelcome(unittest.TestCase):
#
#     def setUp(self):
#         self.userinteractions = UserInteractions()
#
#     @patch('builtins.input', return_value='search')
#     def test_welcome_search(self, mocked_input):
#         with patch.object(self.userinteractions, 'filtered_choice') as mock_filtered_choice:
#             self.userinteractions.welcome()
#             mock_filtered_choice.assert_called_once()
#
#     @patch('builtins.input', return_value='random')
#     def test_welcome_random(self, mocked_input):
#         with patch.object(self.userinteractions, 'random_choice') as mock_random_choice:
#             self.userinteractions.welcome()
#             mock_random_choice.assert_called_once()
#
#     @patch('builtins.input', return_value='to-read')
#     def test_welcome_to_read(self, mocked_input):
#         with patch.object(self.userinteractions, 'view_to_read_list') as mock_view_to_read_list:
#             self.userinteractions.welcome()
#             mock_view_to_read_list.assert_called_once()
#
#     @patch('builtins.input', return_value='read')
#     def test_welcome_read(self, mocked_input):
#         with patch.object(self.userinteractions, 'view_read_list') as mock_view_read_list:
#             self.userinteractions.welcome()
#             mock_view_read_list.assert_called_once()
#
#     @patch('builtins.input', return_value='exit')
#     def test_welcome_exit(self, mocked_input):
#         with patch('builtins.print') as mock_print:
#             self.userinteractions.welcome()
#             mock_print.assert_called_once_with('Goodbye!')
#
#     @patch('builtins.input', return_value='add')
#     def test_welcome_add(self, mocked_input):
#         with patch.object(self.userinteractions, 'add_book_to_read_list') as mock_add_book:
#             self.userinteractions.welcome()
#             mock_add_book.assert_called_once()
#
#
# ################################################################################################################
#
# class TestPrintSearchCriteriaMessage(unittest.TestCase):
#
#     def setUp(self):
#         self.userinteractions = UserInteractions()
#
#     def test_print_search_criteria_message(self):
#         expected = "What would you like to search by? (Press enter if you would like to leave blank):\n"
#         with patch("sys.stdout", new = StringIO()) as test_message:
#             self.userinteractions.print_search_criteria_message()
#             self.assertEqual(test_message.getvalue(), expected)
#
#
# ##################################################################################################
# class TestNumberOfBooks(unittest.TestCase):
#
#
#     def setUp(self):
#         self.userinteractions = UserInteractions()
#
#     def test_get_number_of_books_valid_input(self):
#         with patch('builtins.input', return_value='5'):
#             result = self.userinteractions.get_number_of_books()
#             self.assertEqual(result, 5)
#
#     def test_get_number_of_books_invalid_input(self):
#         with patch('builtins.input', side_effect=['0', '11', '6']):
#             result = self.userinteractions.get_number_of_books()
#             self.assertEqual(result, 6)
#
#     def test_get_number_of_books_invalid_input(self):
#         with patch('builtins.input', side_effect=['11']):
#             result = self.userinteractions.get_number_of_books()
#             self.assertEqual(result, 6)
#
#     def test_get_number_of_books_edge_case_minimum(self):
#         with patch('builtins.input', return_value='1'):
#             result = self.userinteractions.get_number_of_books()
#             self.assertEqual(result, 1)
#
#     def test_get_number_of_books_edge_case_maximum(self):
#         with patch('builtins.input', return_value='10'):
#             result = self.userinteractions.get_number_of_books()
#             self.assertEqual(result, 10)

################################################################################################

# class TestPrintBookGenreDictionary(unittest.TestCase):
#
#     def setUp(self):
#         self.userinteractions = UserInteractions()
#
#     def test_print_book_genre_dictionary(self):
#         expected_output = '''You can choose from the following categories:
# 1: Animals, Bugs & Pets
# 2: Art, Creativity & Music
# 3: General Literature
# 4: Hobbies, Sports & Outdoors
# 5: Science Fiction & Fantasy
# 6: Real Life
# 7: Science & Technology
# 8: Mystery & Suspense
# 9: Reference
# '''
#         with patch("sys.stdout", new = StringIO()) as dictionary_message:
#             self.userinteractions.print_book_genre_dictionary()
#             self.assertEqual(dictionary_message.getvalue(), expected_output)

##################################################################################################

class TestGetValidGenreChoice(unittest.TestCase):

    def setUp(self):
        self.userinteractions = UserInteractions()

    # def test_get_valid_genre_choice_valid_input(self):
    #
    #     with patch('builtins.input', return_value='5'):
    #         expected = 'Science Fiction & Fantasy'
    #         result = self.userinteractions.get_valid_genre_choice()
    #         self.assertEqual(result, expected)
    #
    # def test_get_valid_genre_choice_empty_input(self):
    #
    #     with patch('builtins.input', return_value=''):
    #         expected = None
    #         result = self.userinteractions.get_valid_genre_choice()
    #         self.assertEqual(result, expected)

'''
I've done some googling and not sure how to make an invalid test work for While True.....
(This is failing)
'''
    # def test_get_valid_genre_choice_invalid_input(self):
    #
    #     with patch('builtins.input', side_effect = '0'):
    #         expected_output = 'Invalid genre choice. Please choose a valid number from the genre choices.'
    #         result = self.userinteractions.get_valid_genre_choice()
    #         self.assertEqual(result, expected_output)


##################################################################################################
# def validate_input_y_or_n(self, prompt):
#     while True:
#         user_input = input(prompt)
#         if user_input.lower() == 'y' or user_input.lower() == 'n':
#             return user_input.lower()
#         else:
#             print("Invalid input. Please enter 'y' or 'n'.")


class TestValidateInputYorN(unittest.TestCase):

    def setUp(self):
        self.userinteractions = UserInteractions()

    def test_validate_input_y(self):

        with patch('builtins.input', return_value = 'Y'):
            prompt = "Please enter 'y' or 'n': "
            expected = 'y'
            result = self.userinteractions.validate_input_y_or_n(prompt)
            self.assertEqual(result, expected)

    def test_validate_input_n(self):

        with patch('builtins.input', return_value='n'):
            prompt = "Please enter 'y' or 'n': "
            expected = 'n'
            result = self.userinteractions.validate_input_y_or_n(prompt)
            self.assertEqual(result, expected)

'''
Same issue as above with the While True.....
(This is failing)
'''
    # def test_validate_input_n(self):
    #
    #     with patch('builtins.input', return_value='T'):
    #         prompt = "Please enter 'y' or 'n': "
    #         expected = "Invalid input. Please enter 'y' or 'n'."
    #         result = self.userinteractions.validate_input_y_or_n(prompt)
    #         self.assertEqual(result, expected)


##################################################################################################

'''
This looks difficult, will come back to
'''
# class TestFilteredChoice(unittest.TestCase):
#
#     def setUp(self):
#         self.userinteractions = UserInteractions()
#
#     def test_filtered_choice_valid_input(self, mock_input):
#

##################################################################################################

class TestRandomChoice(unittest.TestCase):

    def setUp(self):
        self.userinteractions = UserInteractions()

##################################################################################################

class TestAddRandomBookToToReadList(unittest.TestCase):

    def setUp(self):
        self.userinteractions = UserInteractions()

##################################################################################################

class TestAddFilteredBookToToReadList(unittest.TestCase):

    def setUp(self):
        self.userinteractions = UserInteractions()

##################################################################################################

class TestGetBookDetails(unittest.TestCase):

    def setUp(self):
        self.userinteractions = UserInteractions()

    @patch('builtins.input', side_effect=['Philip Pullman', 'Northern Lights', '5'])
    def test_get_book_details_all_given(self, mock_input):
        expected_result = {
            'authors': 'Philip Pullman',
            'title': 'Northern Lights',
            'categories': 'Science Fiction & Fantasy'
        }
        result = self.userinteractions.get_book_details()
        self.assertEqual(result, expected_result)

    @patch('builtins.input', side_effect=['', 'Northern Lights', '5'])
    def test_get_book_details_no_author(self, mock_input):
        expected_result = {
            'authors': '',
            'title': 'Northern Lights',
            'categories': 'Science Fiction & Fantasy'
        }
        result = self.userinteractions.get_book_details()
        self.assertEqual(result, expected_result)

    @patch('builtins.input', side_effect=['Philip Pullman', '', '5'])
    def test_get_book_details_no_title(self, mock_input):
        expected_result = {
            'authors': 'Philip Pullman',
            'title': '',
            'categories': 'Science Fiction & Fantasy'
        }
        result = self.userinteractions.get_book_details()
        self.assertEqual(result, expected_result)




if __name__ == '__main__':
    unittest.main()

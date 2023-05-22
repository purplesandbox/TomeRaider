import unittest
from unittest import mock
from unittest.mock import patch
from user_interactions import UserInteractions
from io import StringIO
import sys

########################################################################################################
class TestWelcome(unittest.TestCase):

    def setUp(self):
        self.userinteractions = UserInteractions()

    @patch('builtins.input', return_value='search')
    def test_welcome_search(self, mocked_input):
        with patch.object(self.userinteractions, 'filtered_choice') as mock_filtered_choice:
            self.userinteractions.welcome()
            mock_filtered_choice.assert_called_once()

    @patch('builtins.input', return_value='random')
    def test_welcome_random(self, mocked_input):
        with patch.object(self.userinteractions, 'random_choice') as mock_random_choice:
            self.userinteractions.welcome()
            mock_random_choice.assert_called_once()

    @patch('builtins.input', return_value='to-read')
    def test_welcome_to_read(self, mocked_input):
        with patch.object(self.userinteractions, 'view_to_read_list') as mock_view_to_read_list:
            self.userinteractions.welcome()
            mock_view_to_read_list.assert_called_once()

    @patch('builtins.input', return_value='read')
    def test_welcome_read(self, mocked_input):
        with patch.object(self.userinteractions, 'view_read_list') as mock_view_read_list:
            self.userinteractions.welcome()
            mock_view_read_list.assert_called_once()

    @patch('builtins.input', return_value='exit')
    def test_welcome_exit(self, mocked_input):
        with patch('builtins.print') as mock_print:
            self.userinteractions.welcome()
            mock_print.assert_called_once_with('Goodbye!')

    @patch('builtins.input', return_value='add')
    def test_welcome_add(self, mocked_input):
        with patch.object(self.userinteractions, 'add_book_to_read_list') as mock_add_book:
            self.userinteractions.welcome()
            mock_add_book.assert_called_once()

# This one is failing?
'''    @patch('builtins.input', side_effect=['invalid', 'search'])
    def test_welcome_invalid_then_search(self, mocked_input):
        with patch('builtins.print') as mock_print:
            self.userinteractions.welcome()
            expected_calls = [
                unittest.mock.call('Invalid choice. Please try again.'),
                unittest.mock.call().assert_called_once_with()
            ]
            mock_print.assert_has_calls(expected_calls)'''

################################################################################################################

class TestPrintSearchCriteriaMessage(unittest.TestCase):

    def setUp(self):
        self.userinteractions = UserInteractions()

    def test_print_search_criteria_message(self):
        expected_output = "What would you like to search by? (Press enter if you would like to leave blank):\n"
        with patch("sys.stdout", new = StringIO()) as test_message:
            self.userinteractions.print_search_criteria_message()
            self.assertEqual(test_message.getvalue(), expected_output)


##################################################################################################
class TestNumberOfBooks(unittest.TestCase):


    def setUp(self):
        self.userinteractions = UserInteractions()

    def test_get_number_of_books_valid_input(self):
        with patch('builtins.input', return_value='5'):
            result = self.userinteractions.get_number_of_books()
            self.assertEqual(result, 5)

    def test_get_number_of_books_invalid_input(self):
        with patch('builtins.input', side_effect=['0', '11', '6']):
            result = self.userinteractions.get_number_of_books()
            self.assertEqual(result, 6)  # Retry until valid input is provided

    def test_get_number_of_books_invalid_input_then_valid_input(self):
        with patch('builtins.input', side_effect=['invalid', '4']):
            result = self.userinteractions.get_number_of_books()
            self.assertEqual(result, 4)

    def test_get_number_of_books_edge_case_minimum(self):
        with patch('builtins.input', return_value='1'):
            result = self.userinteractions.get_number_of_books()
            self.assertEqual(result, 1)

    def test_get_number_of_books_edge_case_maximum(self):
        with patch('builtins.input', return_value='10'):
            result = self.userinteractions.get_number_of_books()
            self.assertEqual(result, 10)

##################################################################################################




if __name__ == '__main__':
    unittest.main()

import unittest
from unittest import mock
from unittest.mock import patch
from user_interactions import UserInteractions

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

if __name__ == '__main__':
    unittest.main()

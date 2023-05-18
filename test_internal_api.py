from unittest import TestCase, main, mock
from internal_api import InternalAPI


class InternalAPITests(TestCase):
    # def test_add_to_to_read_list(self):
    #     self.internal_api = InternalAPI()
    #     to_read = {
    #         'title': 'The Great Gatsby',
    #         'author': 'F. Scott Fitzgerald',
    #         'category': 'Fiction, Non-Fiction & Poetry'
    #     }
    #     expected = 'The Great Gatsby has been added to reading list'
    #     result = self.internal_api.add_to_to_read_list(to_read)
    #     self.assertEqual(expected, result)
    def test_add_to_to_read_list_1(self):
        self.internal_api = InternalAPI()
        to_read = {
            'title': 'The B.F.G',
            'author': 'Rhoal Dahl',
            'category': 'Fiction'
        }
        expected = 'The B.F.G has been added to reading list'
        result = self.internal_api.add_to_to_read_list(to_read)
        self.assertEqual(expected, result)

    # def test_successful_purchase(self):
    #     expected = 'jumper'
    #     result = interaction_with_customer_3_times(money, 'jumper')
    #     self.assertEqual(expected, result)




if __name__ == "__main__":
    main()

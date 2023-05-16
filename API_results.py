import requests
import random
from pprint import pprint
from urllib.error import HTTPError, URLError


class BookFinderAPICalls:
    def __init__(self, user_input):
        self.user_input = user_input
        self.endpoint = 'https://book-finder1.p.rapidapi.com/api/search'
        self.requirement = {
    'X-RapidAPI-Key': 'e42255e58dmsh896e188a4c3b74dp12368fjsn273ec0f1d7ca',
    'X-RapidAPI-Host': 'book-finder1.p.rapidapi.com'
}
        self.relevant_keys = ['authors', 'title', 'categories', 'summary']

    def make_api_request(self):
        try:
            response = requests.get(self.endpoint, params=self.user_input, headers=self.requirement)
            records = response.json()
        except HTTPError as error:
            print(error.status, error.reason)
            exit(1)
        except URLError as error:
            print(error.reason)
            exit(1)
        except TimeoutError:
            print("Request timed out")
            exit(1)
        else:
            return records


    def get_filtered_results(self):
        try:
            books = int(self.user_input['book_num'])
            records = self.make_api_request()
            if records['total_results'] < books:
                raise ValueError
                exit(1)
        except:
            print("The requested number of books to be returned exceeds the number of matching records! Please, try again!")
        else:
            random_sample = random.sample(records['results'], books)
            random_sample_reduced = [{key: d[key] for key in self.relevant_keys} for d in random_sample]
            return random_sample_reduced

    def get_random_result(self):
        records = self.make_api_request()
        random_number = random.randrange(0, len(records['results']))
        random_record = records['results'][random_number]
        random_record_reduced = {key: random_record[key] for key in self.relevant_keys}
        return random_record_reduced


    def get_records(self):

        if self.user_input['filtered_choice']:
            return self.get_filtered_results()

        elif self.user_input['random_choice']:
            return self.get_random_result()

# dictionary passed from UserInteractions class
user_input = {
    'author': None,
    'book_type': 'Fiction',
    'results_per_page': '100',
    'page': '1',
    'lexile-min': 1000,
    'lexile-max':2000,
    'categories': "Mystery & Suspense",
    'book_num': 5,
    'random_choice': False,
    'filtered_choice': True
}

book_finder = BookFinderAPICalls(user_input)
pprint(book_finder.get_records())












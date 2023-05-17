from pprint import pprint
import requests
import random
from urllib.error import HTTPError, URLError

# """
# Definition of the class which deals only with the external https://book-finder1.p.rapidapi.com/api API calls and returns results.
# It takes values from the user input dictionary to initialise the API calls
#
# """
class BookAppAPI:
    def __init__(self):
        self.endpoint = 'https://book-finder1.p.rapidapi.com/api/search'
        self.requirement = {
    'X-RapidAPI-Key': 'e42255e58dmsh896e188a4c3b74dp12368fjsn273ec0f1d7ca',
    'X-RapidAPI-Host': 'book-finder1.p.rapidapi.com'
}
        self.relevant_keys = ['authors', 'title', 'categories', 'summary']
        self.request_params = {'results_per_page': '100', 'page': '1'}

    # """
    # make_api_request method calls the api, based on the user input parameters, handles potential errors and returns the records.
    #
    # """
    def make_api_request(self, user_input):
        try:
            user_input.update(self.request_params)
            response = requests.get(self.endpoint, params=user_input, headers=self.requirement)
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

    # """
    # get_filtered_results method uses make_apy_request method to get the API request results,
    # reduces to the requested number of records, specified by the user, and returns only the relevant information for those.
    #
    # """
    def get_filtered_results(self, user_input):
        try:
            books = int(user_input['book_num'])
            records = self.make_api_request(user_input)
            if records['total_results'] < books:
                raise ValueError
                exit(1)
        except:
            print("The requested number of books to be returned exceeds the number of matching records! Please, try again!")
        else:
            random_sample = random.sample(records['results'], books)
            random_sample_reduced = [{key: d[key] for key in self.relevant_keys} for d in random_sample]
            return random_sample_reduced

    # """
    # get_random_result method uses make_apy_request method to get the API request results,
    # reduces it to a single, randomly chosen record, and returns only the relevant information for it.
    # """
    def get_random_result(self, user_input):
        records = self.make_api_request(user_input)
        random_number = random.randrange(0, len(records['results']))
        random_record = records['results'][random_number]
        random_record_reduced = {key: random_record[key] for key in self.relevant_keys}
        return random_record_reduced




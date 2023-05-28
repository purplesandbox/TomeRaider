import requests
import random
import os


# """
# Definition of the class which deals only with the external https://book-finder1.p.rapidapi.com/api API calls and returns results.
# It takes values from the user input dictionary to initialise the API calls
#
# """
class BookAppAPI:
    def __init__(self):
        self.endpoint = 'https://book-finder1.p.rapidapi.com/api/search'
        self.requirement = {
    'X-RapidAPI-Key': os.getenv('X-RapidAPI-Key'),
    'X-RapidAPI-Host': os.getenv('X-RapidAPI-Host')
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
            if response.status_code != 200:
                response.raise_for_status()
            else:
                records = response.json()
                if records is None:
                    raise ValueError
                if records['total_results'] == 0:
                    raise ValueError
        except ValueError:
            print("No records found for your search criteria. Please, try again")
        except requests.exceptions.HTTPError:
            print("Http Error")
        except requests.exceptions.ConnectionError:
            print("Error Connecting")
        except requests.exceptions.Timeout:
            print("Timeout Error")
        except requests.exceptions.RequestException:
            print("OOps: Something Else")
        else:
            return records

    # """
    # get_filtered_results method uses make_apy_request method to get the API request results,
    # reduces to the requested number of records, specified by the user, and returns only the relevant information for those.
    #
    # """
    def get_filtered_results(self, user_input):
        books = int(user_input['book_num'])
        records = self.make_api_request(user_input)
        # in case the number of the API returned books is less that the requested, program returns all available ones from the API database
        if records['total_results'] < books:
            return [{key: d[key] for key in self.relevant_keys} for d in records['results']]
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


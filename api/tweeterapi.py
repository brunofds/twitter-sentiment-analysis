import logging
import os
from xmlrpc.client import ResponseError
import pandas as pd

import requests
from authentication import auth

logger = logging.getLogger(__name__)



class Tweets():

    def __init__(self):
        self.lang = 'en'
        self.result_type = 'recent'
        self.count = 100
        self.twfields = ['text', 'created_at']  # TODO Check metadata names on Twitter API
        self.hashtag = 'Corona'
        self.param_query_v2 = 'query'
        self.response_file = 'csv'
        self.dir_files = 'files/'

    def search_query_v2(self, **params):
        url = 'https://api.twitter.com/2/tweets/search/recent?'
        response = None
        
        try:
            response = auth.get_data_apiv1(url, **params)
            logger.info(f"Status Code: {response.status_code}")
            print(response.json())
            auth.generate_bearer_token()
        except requests.RequestException as erro:
            print(erro)
        if not response:
            raise ResponseError(f"It wasn't possible to find data with this parameters: {params} or you are Unauthorized ")

        return response


def remove_character_response(response, separator):
    return response.text.replace(separator, ";")


def _create_dir(folder):
    try:
        os.makedirs(folder, exist_ok=True)
    except OSError as erro:
        logger.error("Can't create destination directiory %s! OSError: %s", folder, erro)
    logger.info(f"Folder '{folder}' created successfully")


def _store_list_csv(filename, folder, response):
    file_and_extension = filename + '.csv'
    filepath = os.path.join(folder, file_and_extension)
    _create_dir(folder)
    df = pd.DataFrame(response.json()['data'], columns=['text', 'created_at'])
    df.to_csv(filepath, sep='|')
    logger.info(
        f"{filename} created successfully in {file_and_extension} folder")
    

def store_response_csv(response, filename, folder, separator='|'):
    cleaned_response = remove_character_response(response, separator='|')
    logger.info(f"Separator '{separator}' removed from response")
    _store_list_csv(filename, folder, response)


def json_response_twitter(response):
    dict_response = response.json()
    return dict_response

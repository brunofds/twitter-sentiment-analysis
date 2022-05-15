from logging import raiseExceptions
from urllib import response
from xmlrpc.client import ResponseError
import requests
import logging
# import logging.config
from authentication import auth
import os
import json
import csv
# from twlogging import logtw

# logger = logtw

# logging.basicConfig(level=logging.INFO)
# ConsoleOutputFormat = logging.Formatter('%(asctime)s %(name)s: %(levelname)s - %(message)s')
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
        except requests.RequestException as e:
            print(e)
        if not response:
            raise ResponseError(f"It wasn't possible find data with this parameters: {params} ")

        return response


def generate_json():
    pass


def remove_character_response(response, separator):
    return response.text.replace("|", ";")


def _json_list_to_csv(json_string):
    list_values = []
    json_text = json.loads(json_string)
    fields = list(json_text.get('data')[0].keys())
    for i in json_text.get('data'):
        list_values.append(list(i.values()))
    return fields, list_values


def _create_dir(folder):
    try:
        os.makedirs(folder, exist_ok=True)
    except OSError as e:
        logger.error("Can't create destination directiory (%s)!" % folder)
    logger.info(f"Folder '{folder}' created successfully")



def _store_list_csv(header, list_values, filename, folder):
    file_and_extension = filename + '.csv'
    filepath = os.path.join(folder, file_and_extension)
    _create_dir(folder)
    with open(filepath, 'w') as f:
        write = csv.writer(f, delimiter='|')
        write.writerow(header)
        write.writerows(list_values)
    logger.info(
        f"{filename} created successfully in {file_and_extension} folder")


def store_response_csv(response, filename, folder, separator='|'):
    cleaned_response = remove_character_response(response, '|')
    _json_list_to_csv(cleaned_response)
    logger.info(f"Separator '{separator}' removed from response")
    fields, list_values = _json_list_to_csv(cleaned_response)
    _store_list_csv(fields, list_values, filename, folder)



    #fields = list(y.get('data')[0].keys())
    #list_values.append([x[0].values() for x in y.get('data')])
    # rows = [x for x in x().get('data').values()]


    # os.path.join(path_out, file_name, "." + '.csv')
    # if response:
    #     with open


def json_response_twitter(response):
    dict_response = response.json()
    return dict_response


def create_lists_by_keys(dict_response, key_response):
    lists_keys = {}
    quant_key_response = len(key_response.values())
    for k, v in key_response.items():
        print(k)
        lists_keys[k] = list()
        for keys in dict_response['statuses']:
            lists_keys[k].append(keys[k])

    return lists_keys

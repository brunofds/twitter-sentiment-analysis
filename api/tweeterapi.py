from logging import raiseExceptions
import requests
import logging
from authentication import auth

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class Tweets():

    def __init__(self):
        self.lang = 'en'
        self.result_type = 'recent'
        self.count = 100
        self.twfields = ['text', 'created_at']  # TODO Check metadata names on Twitter API
        self.hashtag = 'Corona'
        self.param_query_v2 = 'query'
        self.response_file = 'csv'

    # def _generate_query(self, hashtag, **kwargs) -> str:

    #     url_string = f"{self.param_query_v2}={hashtag}"
    #     for k, v in kwargs.items():
    #         if isinstance(v, list):
    #             for i in v:
    #                 str_list = str_list + {i.value}
    #         url_string = url_string + f"&{k}={v}"
    #     logger.info(f"Query generated: {url_string}")
    #     return url_string

    def search_query_v2(self, **params) -> None:
        url = 'https://api.twitter.com/2/tweets/search/recent?'
        try:
            response = auth.get_data_apiv1(url, **params)
            logger.info(f"Status Code: {response.status_code}")
            print(response.json())
        except requests.RequestException as e:
            print(e)


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
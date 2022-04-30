
from http.client import responses
import requests
from os import environ
from dotenv import load_dotenv


load_dotenv()

API_KEY = environ.get('API_KEY')
API_KEY_SECRET = environ.get('API_KEY_SECRET')
BEARER_TOKEN = environ.get('BEARER_TOKEN')
ACCESS_TOKEN = environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = environ.get('ACCESS_TOKEN_SECRET')


# Implementation of a bearer authentication (subclass)
class BearerAuth():
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def _bearer_token_header():
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    return headers


def get_data_apiv1(url, **params):
    # params = {'query': query}
    headers = _bearer_token_header()
    # params = {"query": "corona"}
    return requests.request('GET', url, headers=headers, params=params)




def post_api_v1():
    pass

# def connect_twitterapi(url, auth_bearer):
#     r = requests.get(url, auth=BearerAuth(auth_bearer))
#     if r.status_code == 200:
#         print("200 - SUCCESS RESPONSE")
#     else:
#         print("Probably an error")
#     return r


def use_yaml(yml_file, *argv):
    with open('config.yml', 'r') as cgfile:
        pass
        # data = yaml.safe_load(cgfile)
        # return (data['search_tweets_api_cred']['key_bearer_token'])

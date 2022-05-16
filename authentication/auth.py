import logging
from http.client import responses
from os import environ

import dotenv
import requests
from dotenv import load_dotenv
from requests import auth

load_dotenv()
dotenv_file = dotenv.find_dotenv()
logger = logging

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
    response = requests.request('GET', url, headers=headers, params=params)
    if response.status_code == 401:
        generate_bearer_token()

    return response


def _handle_response_bearer(response):
    if response.status == 401:
        logger.error("There was a problem authenticating your request due to missing or incorrect authentication credentials. Check if your api_key and api_key_secret are right")
        choose = input("Do you want generate another token (y/n)? ")
        if choose == 'y':
            generate_bearer_token()
    return


def generate_bearer_token():
    url = 'https://api.twitter.com/oauth2/token'
    data = {
        'grant_type': 'client_credentials',
    }
    response = requests.post(
        url, data=data, auth=auth.HTTPBasicAuth(API_KEY, API_KEY_SECRET))
    print(f"Response: {response.status_code}")
    if response.status_code == 200:
        logger.info(f"Generate Bearer token Response: {response}")
        bearer_token = response.json()['access_token']
        dotenv.set_key(dotenv_file, 'BEARER_TOKEN', bearer_token)
    else:
        _handle_response_bearer(response)
        logger.info(
            f"You don't have the right permissions to generate de Bearer Token: {response}")


def post_api_v1():
    pass


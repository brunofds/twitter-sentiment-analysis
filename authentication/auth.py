from cgitb import text
import logging
from http.client import responses
from os import environ
from pkgutil import get_data
from xmlrpc.client import ResponseError

import dotenv
import requests
from dotenv import load_dotenv
from requests import auth

load_dotenv(override=True)
dotenv_file = dotenv.find_dotenv()
logger = logging

API_KEY = environ.get('API_KEY')
API_KEY_SECRET = environ.get('API_KEY_SECRET')
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
    load_dotenv(override=True)
    bearer_token = environ.get('BEARER_TOKEN')
    headers = {"Authorization": f"Bearer {bearer_token}"}
    return headers


def _handle_response(response) -> bool:
    new_bearer = False
    logger.info(f"Search API response: {response.text}")
    if response is not None:
        if response.status_code == 200:
            logger.info(f"Response was genererated with succes. response.status_code = {response.status_code}")
        if response.status_code == 401:
            logger.info(f"There was a problem authenticating your request due to missing or incorrect authentication credentials.")
            if str(input("Do you want generate another token (y/n)? ")).lower() == 'y':
                new_bearer = generate_bearer_token()
                return new_bearer
    else:
        logger.info("The response from search tweet was None")
        raise ResponseError("The Search API response was bad")
    
    return new_bearer


def get_data_apiv1(url, **params):
    headers = _bearer_token_header()
    
    try:
        response = requests.request('GET', url, headers=headers, params=params)
        if _handle_response(response):
            return get_data_apiv1(url, **params)
        return response
    except requests.HTTPError as e:
        logger.error(f"Exception caught on Tweeter API: {e}")


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
        return True
    else:
        logger.info(
            f"You don't have the right permissions to generate de Bearer Token: {response}")
        return False


def post_api_v1():
    pass


import os
import requests
from requests_oauthlib import OAuth1
import json
import yaml
import numpy as np


# Implementation of a bearer authentication (subclass)
class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def use_yaml(yml_file, *argv):
    with open('config.yml', 'r') as cgfile:
        data = yaml.safe_load(cgfile)
        return (data['search_tweets_api_cred']['key_bearer_token'])


def connect_twitterapi(url, auth_bearer):
    r = requests.get(url, auth=BearerAuth(auth_bearer))
    if r.status_code == 200:
        print("200 - SUCCESS RESPONSE")
    else:
        print("Probably an error")
    return r

#def create_url_search(parameters):
def create_url_search(parameters):
    url = 'https://api.twitter.com/1.1/search/tweets.json?'

    if len(parameters.keys()) > 0:
        url_parameters = url + 'q=' + list(parameters.values())[0]
        for p in range(1, len(parameters.keys()), 1):
            url_parameters = url_parameters + '&' + list(parameters.values())[p]

    return url_parameters

def json_response_tweeter(respose):
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

    print(lists_keys)



if __name__ == '__main__':

    # Search Parameters
    parameters = dict()
    parameters['hashtag_search'] = "'%23Corona'"
    parameters['language'] = 'lang=en'
    parameters['recent'] = 'result_type=recent'
    parameters['quant'] = 'count=10'
    #list_parameters = list()
    #list_parameters.extend([hashtag_search, language, recent, quant])

    # Yaml parameters
    api_name = 'search_tweets_api_cred'
    bearer_token = 'key_bearer_token'
    config_name = 'config.yml'

    # Tweeter lists
    tweeter_texts = list()
    tweeter_created_time = list()

    # Response keys
    key_response = dict()
    key_response['text'] = 'text'
    key_response['created_at'] = 'created_at'



    # Creating the url
    url = create_url_search(parameters)
    print(url)

    # Get the bearer auth over yaml file
    bearer_auth = use_yaml(config_name, api_name, bearer_token)

    # Connect Twitter API (with bearer auth)
    response = connect_twitterapi(url, bearer_auth)

    # Get the dict response
    dict_response = json_response_tweeter(response)

    # Create list of tweets and dates
    create_lists_by_keys(dict_response, key_response)

    # get the keys_response and assigns to df
    




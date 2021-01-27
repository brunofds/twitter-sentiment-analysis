import os
import requests
import json
import yaml
import numpy as np
import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt


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

    print(url_parameters)
    return url_parameters

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


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
    return input_txt


def clean_tweets(tweets):
    # remove twitter Return handles (RT @xxx:)
    tweets = np.vectorize(remove_pattern)(tweets, "RT @[\w]*:")

    #     # Remove break lines \n
    #     tweets = np.vectorize(remove_pattern)(tweets, "\n")

    # remove twitter handles (@xxx)
    tweets = np.vectorize(remove_pattern)(tweets, "@[\w]*")

    # remove URL links (httpxxx)
    tweets = np.vectorize(remove_pattern)(tweets, "https?://[A-Za-z0-9./]*")

    # remove special characters, numbers, punctuations (except for #)
    tweets = np.core.defchararray.replace(tweets, "[^a-zA-Z]", " ")
    # tweets = np.core.defchararray.replace(tweets, r"[^\w\s]", " ")
    # tweets = np.vectorize(remove_pattern)(tweets, "")

    return tweets


def sentiment_scores(sentence):
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # oject gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)

    # decide sentiment as positive, negative and neutral using the compound value
    if sentiment_dict['compound'] >= 0.05:
        return "positive"

    elif sentiment_dict['compound'] <= - 0.05:
        return "negative"

    else:
        return "neutral"


if __name__ == '__main__':

    # Search Parameters
    parameters = dict()
    #parameters['hashtag_search'] = "'%23Corona'"
    hashtag = input("Input the hashtag you want to analyse the sentiment: ")
    parameters['hashtag_search'] = "%23" + hashtag
    parameters['language'] = 'lang=en'
    parameters['recent'] = 'result_type=recent'
    parameters['quant'] = 'count=150'
    #list_parameters = list()
    #list_parameters.extend([hashtag_search, language, recent, quant])

    # Yaml parameters
    api_name = 'search_tweets_api_cred'
    bearer_token = 'key_bearer_token'
    config_name = 'config.yml'

    # Response keys (inside statuses there is a dictionary list)
    key_response = dict()
    key_response['text'] = 'text'
    key_response['created_at'] = 'created_at'

    # Creating the url
    url = create_url_search(parameters)
    #print(url)

    # Get the bearer auth over yaml file
    bearer_auth = use_yaml(config_name, api_name, bearer_token)

    # Connect Twitter API (with bearer auth)
    response = connect_twitterapi(url, bearer_auth)

    # Get the dict response
    dict_response = json_response_twitter(response)

    # Create list of tweets and dates
    lists_keys = create_lists_by_keys(dict_response, key_response)

    # get the text responses and assigns to df
    d = {'texts': lists_keys['text']}
    df = pd.DataFrame(data=d)
    print(df)

    # Cleaning the data
    df['texts'] = clean_tweets(df['texts'])

    # Sentimental analysis using Vader
    #analyser = SentimentIntensityAnalyzer()
    df['classification'] = df['texts'].apply(sentiment_scores)
    print(df)

    # Extra columns
    d = {'created_at': lists_keys['created_at']}
    df['created_at'] = pd.DataFrame(data=d)
    print(df)

    # Saving in a excel file
    df.to_excel(hashtag + "twitterSentimentals.xlsx", index=False)

    # Plotting horizontal bar
    df.groupby('classification')['texts'].nunique().plot(kind='bar')
    plt.show()









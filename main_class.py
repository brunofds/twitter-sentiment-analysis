import requests
import os
import yaml
import json
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import numpy as np
import re

consumer_key = ''
consumer_secret = ''

response = requests.get('https://api.twitter.com/1.1/search/tweets.json?', params={'name': 'Bearer'})



class Twitterpy():

    def __init__(self, bearer_token=None, url=r'https://api.twitter.com/1.1/search/tweets.json?'):
        self.bearer_token = bearer_token
        self.url = url

    def use_yaml_bearer(self, name_yml_file=None, api_name=None, key_bearer_token=None):
        self.name_yml_file = name_yml_file
        self.api_name = api_name
        self.key_bearer_token = key_bearer_token

        with open(self.name_yml_file, 'r') as cgfile:
            data = yaml.safe_load(cgfile)
            self.bearer_token = data[self.api_name][self.key_bearer_token]
            print("Bearer Token:", self.bearer_token)

        self.headers = {"Authorization": "Bearer {}".format(self.bearer_token)}

        return (self.bearer_token)

    def generate_url(self, language='en', result_type='recent', count_tweets=10, hashtag='%23Corona'):
        self.language = language
        self.result_type = result_type
        self.count_tweets = count_tweets
        self.hashtag = hashtag

        lang = 'lang={}'.format(self.language)
        count = 'count={}'.format(self.count_tweets)
        result_type = 'result_type={}'.format(self.result_type)
        url_search = '{}q={}&{}&{}&{}'.format(self.url, self.hashtag, lang, result_type, count)
        print(url_search)

        return url_search


    def get_response(self, url_search):
        response = requests.request('GET', url_search, headers=self.headers)

        print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)

        return response

    # Statuses
    def create_lists_by_keys(self, dict_response, key_response):
        lists_keys = {}
        quant_key_response = len(key_response.values())
        for k, v in key_response.items():
            print(k)
            lists_keys[k] = list()
            for keys in dict_response['statuses']:
                lists_keys[k].append(keys[k])

        return lists_keys

    def sentiment_scores(self, sentence):
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

    def clean_tweets(self, tweets):

        def remove_pattern(input_txt, pattern):
            r = re.findall(pattern, input_txt)
            for i in r:
                input_txt = re.sub(i, '', input_txt)
            return input_txt

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



def use_yaml_bearer(yml_file, api_name, key_bearer_token):

    with open(yml_file, 'r') as cgfile:
        data = yaml.safe_load(cgfile)
        bearer_token = data[api_name][key_bearer_token]
        print("Bearer Token:", bearer_token)
        return (bearer_token)


def get_response(key_bearer_token):
    # https://api.twitter.com/2/tweets/search/recent?
    headers = {"Authorization": "Bearer {}".format(key_bearer_token)}
    query = "%23Corona&result_type=recent"
    #tweet_fields = "tweet.fields=lang,author_id"
    url = "https://api.twitter.com/1.1/search/tweets.json?q={}".format(
                              query)
    tweet_fields = "tweet.fields=author_id"

    response = requests.request('GET', url, headers=headers)

    print(response.status_code)
    # if response.status_code != 200:
    #     raise Exception(response.status_code, response.text)
    return response


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return rbearer_token


if __name__ == '__main__':

    # 1- Input Hashtag
    hashtag = input("Input the hashtag you want to analyse:")

    # 2 - Object instance
    tweeters = Twitterpy()

    # 3 - Authorization using key bearer token
    bearer = tweeters.use_yaml_bearer(name_yml_file='config.yml', api_name='search_tweets_api_cred',
                             key_bearer_token='key_bearer_token')

    # 4 -  Generate URL Search
    # count_tweets (max=100), language, result_type (recent, mixed, popular)
    url_search = tweeters.generate_url(count_tweets=15, hashtag=hashtag)

    # 5 - Get the response
    response = tweeters.get_response(url_search)
    json_response = response.json()
    print(json_response)

    # 5 - Response keys (inside statuses there is a dictionary list)
    key_response = dict()
    key_response['text'] = 'text'
    key_response['created_at'] = 'created_at'
    key_response['id'] = 'id'

    # 6 - Create list keys
    lists_keys = tweeters.create_lists_by_keys(json_response, key_response)

    # 7 - get the text responses and assigns to df
    d = {'texts': lists_keys['text']}
    df = pd.DataFrame(data=d)
    print(df)

    # 8 -  Cleaning the tweets
    df['texts'] = tweeters.clean_tweets(df['texts'])

    # 9 -  Sentimental analysis using Vader
    #analyser = SentimentIntensityAnalyzer()
    df['classification'] = df['texts'].apply(tweeters.sentiment_scores)
    print(df)

    # 10 - Extra columns
    d = {'created_at': lists_keys['created_at']}
    df['created_at'] = pd.DataFrame(data=d)
    print(df)

    d = {'id': lists_keys['id']}
    df['id'] = pd.DataFrame(data=d)
    df['id'] = df['id'].astype(str)
    print(df)

    # 11 - Saving in a excel file
    df.to_excel(hashtag + "twitterSentimentalsv2.xlsx", index=False)

    # 12 - Plotting horizontal bar
    df.groupby('classification')['texts'].nunique().plot(kind='bar')
    plt.show()



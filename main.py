from api import tweeterapi
import json

# import os
# import requests
# import json
# import yaml
# import pandas as pd
# import re
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# import matplotlib.pyplot as plt


# 1 - Split authentication functions in another file
# 2 - Split the tweeter options to get tweets
# 3 - Split the generation of file with tweets (clean, data and metadata)
# 4 - Split the ML to define the tweets
# TIP: Replace delimiters o tweets before saving on csv

def main():

    # hashtag = input("Input the hashtag you want to analyse the sentiment: ")
    tw_obj = tweeterapi.Tweets()
    response = tw_obj.search_query_v2(**{'query': '(#Corona) lang:en', 'tweet.fields': [{'lang': 'en'}], 'max_results': 10})
    if response:
        print(response.json())

    # # Yaml parameterscorona
    # api_name = 'search_tweets_api_cred'
    # bearer_token = 'key_bearer_token'
    # config_name = 'config.yml'

    # # Response keys (inside statuses there is a dictionary list)
    # key_response = dict()
    # key_response['text'] = 'text'
    # key_response['created_at'] = 'created_at'

    # # Creating the url
    # url = create_url_search(parameters)
    # #print(url)

    # # Get the bearer auth over yaml file
    # bearer_auth = use_yaml(config_name, api_name, bearer_token)

    # # Connect Twitter API (with bearer auth)
    # response = connect_twitterapi(url, bearer_auth)

    # # Get the dict response
    # dict_response = json_response_twitter(response)

    # # Create list of tweets and dates
    # lists_keys = create_lists_by_keys(dict_response, key_response)

    # # get the text responses and assigns to df
    # d = {'texts': lists_keys['text']}
    # df = pd.DataFrame(data=d)
    # print(df)

    # # Cleaning the data
    # df['texts'] = clean_tweets(df['texts'])

    # # Sentimental analysis using Vader
    # #analyser = SentimentIntensityAnalyzer()
    # df['classification'] = df['texts'].apply(sentiment_scores)
    # print(df)

    # # Extra columns
    # d = {'created_at': lists_keys['created_at']}
    # df['created_at'] = pd.DataFrame(data=d)
    # print(df)

    # # Saving in a excel file
    # df.to_excel(hashtag + "twitterSentimentals.xlsx", index=False)

    # # Plotting horizontal bar
    # df.groupby('classification')['texts'].nunique().plot(kind='bar')
    # plt.show()


if __name__ == '__main__':
    main()

import csv
import pandas as pd
import numpy as np
from pathlib import Path
import os
import re
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)
# from twlogging import logtw

# logger = logtw

class Twclassification():
    pass


def _load_csv_to_df(path_file, file_name):
    path_folder = os.path.join(path_file, file_name + '.csv')
    print(path_folder)
    # file = 'files/tweets_csv_out/tweets_out.csv'
    with open(path_folder, 'r') as file:
        df = pd.read_csv(file, sep='|', index_col=0)
    print(df)
    return df
    #logger.info("The csv data was read by Pandas")


def _clean_tweets(tweets_df):
    # remove twitter Return handles (RT @xxx:)
    tweets = tweets_df['text']

    # Remove break lines
    tweets = re.sub(r'\n', ' ', tweets)
    tweets = re.sub(r'\t', ' ', tweets)
    tweets = re.sub(r'\n\r', ' ', tweets)
    tweets = re.sub(r'\r', ' ', tweets)
    tweets = np.vectorize(remove_pattern)(tweets, "RT @[\w]*:")

    # remove twitter handles (@xxx)
    tweets = np.vectorize(remove_pattern)(tweets, "@[\w]*")

    # remove URL links (httpxxx)
    tweets = np.vectorize(remove_pattern)(tweets, "https?://[A-Za-z0-9./]*")

    # remove special characters, numbers, punctuations (except for #)
    tweets = np.core.defchararray.replace(tweets, "[^a-zA-Z]", " ")  # type: ignore
    
    return tweets


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
    return input_txt


def _sentiment_scores(sentence):
    # Create a SentimentIntensityAnalyzer object.
    analyser = SentimentIntensityAnalyzer()
    sentiment_dict = analyser.polarity_scores(sentence['text'])

    # decide sentiment as positive, negative and neutral using the compound value
    if sentiment_dict['compound'] >= 0.05:
        return "positive"
    elif sentiment_dict['compound'] <= - 0.05:
        return "negative"
    else:
        return "neutral"


def _write_df_csv(df, path_file, file_name):
    path_folder = os.path.join(path_file, file_name + '.csv')
    try:
        df.to_csv(path_folder, sep='|')
        logger.info("The file with sentiment analysis was generated ")
    except OSError:
        logger.error("It was not possible to create the sentiment file")


def _write_df_json(df, path_file, file_name):
    path_folder = os.path.join(path_file, file_name + '.json')
    try:
        df.to_json(path_folder)
        logger.info("The file with sentiment analysis was generated ")
    except OSError:
        logger.error("It was not possible to create the sentiment file")


def classify_sentiment(folder, csv_name, csv_out):
    df = _load_csv_to_df(folder, csv_name)

    # Clean text
    df['text_cleaned'] = df.apply(_clean_tweets, axis=1)
    logger.info("The tweets have been cleaned")

    # Apply sentiment analysis
    df['sentiment'] = df.apply(_sentiment_scores, axis=1)
    logger.info("The sentiment analysis has finished")

    # Write the results on csv out file
    _write_df_csv(df, folder, csv_out)
    print(df)


def main(root_folder):
    pass


if __name__ == '__main__':
    main(Path(__file__).parent.parent)

import logging
from api import tweeterapi
from classification import tweets_classification


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def main():
    logger.info("Iniciando a operação")
    csv_name = 'tweets_out'
    csv_sentiment_out = 'sentimentanalysed'
    folder = 'files/tweets_csv_out'

    # hashtag = input("Input the hashtag you want to analyse the sentiment: ")
    tw_obj = tweeterapi.Tweets()
    response = tw_obj.search_query_v2(**{'query': '(#Corona) lang:en', 'tweet.fields': 'text,created_at', 'max_results': 10})
    print(response)
    tweeterapi.store_response_csv(response, csv_name, folder)

    # Read csv file and define the sentiment analyse
    tweets_classification.classify_sentiment(folder, csv_name, csv_sentiment_out)

    # Build a Docker image and store on repository

    # With jenkins and Terraform, create a EC2 Instance

    # With Jenkins, to build the pipeline that install e configurate Python with Docker

    # # Plotting horizontal bar
    # df.groupby('classification')['texts'].nunique().plot(kind='bar')
    # plt.show()


if __name__ == '__main__':
    main()

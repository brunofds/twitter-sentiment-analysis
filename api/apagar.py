from logging import raiseExceptions
import requests
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class Tweets():
    def __init__(self):
        self.params = {
            'lang': 'en',
            'result_type': 'recent',
            'count': 100
        }
        self.twfields = ['text', 'created_at']  # TODO Check metadata names on Twitter API
        self.url = ''
        self.hashtag = 'Corona'

    def _generate_url_search_v1(self, params_tuple: list) -> str:
        query_param = 'q='
        url = 'https://api.twitter.com/1.1/search/tweets.json?'
        url_complete = url + query_param + "&".join(params_tuple)
        return url_complete

    def search_query_v1(self, word: str, lang: str, result_type: str, count_tws: int) -> None:
        search_params = [word, lang, result_type, str(count_tws)]
        url = self._generate_url_search_v1(search_params)
        print(url)


def main():
    tweet = Tweets()
    url = tweet.search_query_v1('teste', 'en', 'recent', 100)


if __name__ == '__main__':
    main()

{
    "query": {"word": "%23Corona", "lang": "en", "count": 100},
    "tweet.fields": ["text", "created_at", "id"],
    "lang": "en",
    "result_type": "recent",
    "count": 100
}
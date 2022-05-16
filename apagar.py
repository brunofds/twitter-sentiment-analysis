from http.client import responses
import requests
from os import environ
import dotenv
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

from authentication.auth import BearerAuth


load_dotenv()
dotenv_file = dotenv.find_dotenv()

API_KEY = environ.get('API_KEY')
API_KEY_SECRET = environ.get('API_KEY_SECRET')
BEARER_TOKEN = environ.get('BEARER_TOKEN')
ACCESS_TOKEN = environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = environ.get('ACCESS_TOKEN_SECRET')
APAGAR = environ.get('APAGAR')

# environ.update(APAGAR='troquei')
# dotenv.set_key(dotenv_file, "APAGAR", 'TROQUEI')

data = {
        'grant_type': 'client_credentials',
    }
url = 'https://api.twitter.com/oauth2/token'
response = requests.post(url, data=data, auth=HTTPBasicAuth(API_KEY, API_KEY_SECRET))
print(response)
bearer_token = response.json()['access_token']
print(bearer_token)

# environ.update(BEARER_TOKEN='')
dotenv.set_key(dotenv_file, "BEARER_TOKEN", bearer_token)
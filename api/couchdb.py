from http.cookiejar import CookieJar
import requests
import json

from requests.cookies import RequestsCookieJar
from requests.models import Response

from config import settings

headers = {'Content-type': 'application/json'}
host = settings.couchdb.HOST

def login() -> Response:

    response = requests.post(f"{host}/_session",
                             headers={'Content-type':'application/x-www-form-urlencoded'},
                             data={'name': settings.COUCHDB_USER,
                                   'password': settings.COUCHDB_PASSWORD})
    response.raise_for_status()

    return response.cookies

cookies = login()

def upsert(payload: dict,
           db : str,
           docid):
    
    response = requests.get(f"{host}/{db}/{docid}")

    rev = json.loads(response.text)['_rev'] if response.status_code == 200 else None

    response = requests.put(f"{host}/{db}/{docid}",
                            cookies = cookies,
                            headers = headers,
                            params = {'rev': rev},
                            json = payload)

    response.raise_for_status()

def insert(payload : dict,
           db : str,
           docid = None,
           ignore_duplicates = False):
    
    response = requests.put(f"{host}/{db}" + f"/{docid}" if docid else "",
                            headers = headers,
                            json = payload)
    
    if response.status_code == 409:
        if not ignore_duplicates:
            response.raise_for_status()
    else:
        response.raise_for_status()


# def upsert(id, payload: dict) -> dict:
#     None

# def upload_tweets(tweets: dict, user : str):

#     for tweet in tweets['data']:
        
#         headers = {'Content-type': 'application/json'}

#         tweet_id = tweet.pop("id")
#         response = requests.get(f"{host}/tweets/{tweet_id}",
#                                 auth = )
        
#         rev = json.loads(response.text)['_rev'] if response.status_code == 200 else None

#         tweet['username'] = user

#         response = requests.put(f"{host}/tweets/{tweet_id}",
#                                 headers = headers,
#                                 params = {'rev': rev},
#                                 auth = HTTPBasicAuth(settings.COUCHDB_USER, 
#                                                      settings.COUCHDB_PASSWORD),
#                                 json = tweet)
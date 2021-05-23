from os import umask
import requests
from requests.auth import HTTPBasicAuth

import json
from config import settings

def load_tweets(user_id: int, since_id: int = None) -> dict:

    url = f'https://api.twitter.com/2/users/{user_id}/tweets'
    headers = {"Authorization": f"Bearer {settings.BEARER_TOKEN}"}

    params = {'tweet.fields': 'in_reply_to_user_id,created_at',
              'max_results': 100,
              'start_time': '2021-01-01T00:00:00Z'}

    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print(response.request.url)
        print(response.request.headers)
        print(response.request.body)
        

def upload_tweets(tweets: dict, user : str):

    for tweet in tweets['data']:
        
        headers = {'Content-type': 'application/json'}

        tweet_id = tweet.pop("id")
        response = requests.get(f"http://localhost:5984/tweets/{tweet_id}",
                                auth = HTTPBasicAuth(settings.COUCHDB_USER, 
                                                     settings.COUCHDB_PASSWORD))
        
        rev = json.loads(response.text)['_rev'] if response.status_code == 200 else None

        tweet['username'] = user

        response = requests.put(f"http://localhost:5984/tweets/{tweet_id}",
                                headers = headers,
                                params = {'rev': rev},
                                auth = HTTPBasicAuth(settings.COUCHDB_USER, 
                                                     settings.COUCHDB_PASSWORD),
                                json = tweet)

def load_user(username: str) -> dict:

    url = f'https://api.twitter.com/2/users/by'

    headers = {"Authorization": f"Bearer {settings.BEARER_TOKEN}"}

    params = {'usernames': username}
    response = requests.request("GET", url, params=params, headers=headers)
    
    if response.status_code == 200:
        return json.loads(response.text)['data']
    else:
        print(response.status_code)
        print(response.text)


user = load_user('gdarruda')
tweets = load_tweets(user[0]['id'])
print(json.dumps(tweets, indent=4))
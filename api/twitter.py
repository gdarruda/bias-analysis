from config import settings

import json
import typing

import requests
from requests.models import Response

headers = {"Authorization": f"Bearer {settings.twitter.BEARER_TOKEN}"}

def get(url: str, params: dict, headers: dict) -> Response:

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    return response

def get_user_info(username: typing.List[str]) -> dict:

    url = 'https://api.twitter.com/2/users/by'

    params = {'usernames': ",".join(username)}
    response = get(url, params=params, headers=headers)

    return json.loads(response.text)['data']

def load_tweets(user_id: int, 
                since_id: int = None) -> list:

    url = f'https://api.twitter.com/2/users/{user_id}/tweets'

    start_time = settings.crawler.BASE_DATE if not since_id else None
 
    params = {'tweet.fields': 'in_reply_to_user_id,created_at',
              'max_results': 100,
              'start_time': start_time,
              'since_id': since_id}

    def load_tweets_token(tweets: list, 
                          token: typing.Optional[str]) -> list:
        
        if token:
            response = get(url,
                           params={**params, 
                                   **{'pagination_token': token}},
                           headers=headers)

            response.raise_for_status()
            content = json.loads(response.text)

            return load_tweets_token(tweets + content['data'],
                                     content['meta'].get('next_token'))

        else:
            return tweets

    response = get(url, params=params, headers=headers)
    content = json.loads(response.text)

    return load_tweets_token(content['data'],
                             content['meta'].get('next_token'))

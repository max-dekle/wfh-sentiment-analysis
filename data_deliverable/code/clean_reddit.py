import requests
import requests.auth
import sqlite3 # TODO do we want to dump to a database eventually?
import os
import json
import time
from datetime import date
import pandas as pd
import re
from unidecode import unidecode

CLIENT_ID = "7HrWBdmYr7EOQXTDkjjFBw"
DEVICE_ID = "UFC2D2IFPF"
APP_SECRET = os.environ.get("REDDIT_APP_SECRET")
USER_AGENT = "osx:remotersanalysis:v0.0.1 (by /u/thenewbie_dev)"

SCORE_THRESHOLD = 200 # threshold below which to ignore posts

SUBREDDITS = ['experienceddevs', 'programming', 'cscareerquestions']
KEYWORDS = ['remote work', 'work from home', 'WFH']


def acquire_auth_token(client_auth):
    post_data = {
        #"grant_type": f"https://oauth.reddit.com/grants/installed_client&\device_id={DEVICE_ID}",
        "grant_type": "client_credentials",
        "device_id": DEVICE_ID,
    }
    headers = {"User-Agent": USER_AGENT}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    # TODO: if response code not ok, throw up or something
    r_json = response.json()
    print(r_json)
    return r_json['access_token'], r_json['token_type'], response.headers

def revoke_token(client_auth, token):
    post_data = {
        "token": token
    }
    headers = {"User-Agent": USER_AGENT}

    # auth=client_auth,
    response = requests.post("https://www.reddit.com/api/v1/revoke_token", auth=client_auth, headers=headers, data=post_data)
    return response


def main():
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, APP_SECRET)
    assert APP_SECRET, "App secret not set"

    token, type, resp_headers = acquire_auth_token(client_auth)
    headers = {"Authorization": f"{type} {token}", "User-Agent": USER_AGENT}

    # conduct search
    result_articles = []
    result_sentiment_ratings = []
    seen_fullnames = set()
    for subreddit in SUBREDDITS:
        for keyword in KEYWORDS:
            done = False
            after = None
            while not done:
                # check we aren't being rate-limited
                if int(resp_headers['X-Ratelimit-Remaining']) < 2:
                    wait_time = resp_headers['X-Ratelimit-Reset'] + 1
                    print(f"being rate limited, sleeping for {wait_time} seconds")
                    time.sleep(wait_time)
                
                search_params = {"q":{keyword}, "sort": "top", "t":"all", "limit": 100, "restrict_sr": True, "after": after}
                search_resp = requests.get(f"https://oauth.reddit.com/r/{subreddit}/search", headers=headers, params=search_params)
                resp_headers = search_resp.headers
                
                after = search_resp.json()['data']['after']
                if after is None:
                    done = True
                
                resp_data = search_resp.json()['data']['children']
                for post in resp_data:
                    post_data = post['data']
                    
                    if post_data['name'] in seen_fullnames:
                        continue
                    seen_fullnames.add(post_data['name'])
                    
                    if not post_data['is_self']:
                        continue
                    if post_data['score'] < SCORE_THRESHOLD:
                        done = True
                        break

                    post_date = date.fromtimestamp(post_data['created'])
                    result_articles.append({
                        'ID': post_data['name'],
                        'URL': post_data['url'],
                        'DATE': post_date.isoformat(),
                        'PLAIN_TEXT': post_data['selftext'],
                        'SOURCE': f"Reddit /r/{subreddit}"
                    })
                    result_sentiment_ratings.append({
                        'ID': post_data['name'],
                        'METHOD': "reddit_post_score",
                        'RATING': post_data['score'],
                    })

    with open('reddit_articles.json', 'w') as outfile:
        json.dump(result_articles, outfile)
    
    with open('reddit_sentiment_ratings.json', 'w') as outfile:
        json.dump(result_sentiment_ratings, outfile)

    print(f"recovered {len(result_articles)} posts with scores above {SCORE_THRESHOLD}")


   
    # search_params = {"q":"Remote", "sort": "top", "t":"all", "limit": 2, "restrict_sr": True}
    # search_1_resp = requests.get("https://oauth.reddit.com/r/programming/search", headers=headers, params=search_params)
    # s1_json = search_1_resp.json()
    # print(s1_json.keys())
    # print(len(s1_json['data']['children']))
    # print(s1_json['data']['children'][0]['data'].keys())
    # post_0 = s1_json['data']['children'][0]['data']
    # print(s1_json['data']['children'][0]['kind'])
    # print(post_0['title'])
    # print(post_0['is_self']) # we want this to always be true
    # print(post_0['created']) # unix timestamp
    # print(post_0['score']) # net upvotes, should be above some threshold
    # print(post_0['url'])
    # print(post_0['is_self']) # we want this to always be true

    # be a good citizen
    revoke_resp = revoke_token(client_auth, token)

    # do the same data cleaning as on guardian
    # TODO break this out into another file?

    df = pd.read_json('reddit_articles.json')

    df.info()
    df['PLAIN_TEXT'] = df['PLAIN_TEXT'].apply(lambda x: re.sub('\n', '', x))
    df['PLAIN_TEXT'] = df['PLAIN_TEXT'].apply(lambda x: re.sub('<.*?>', '', x))
    df['PLAIN_TEXT'] = df['PLAIN_TEXT'].apply(lambda x: unidecode(str(x)))
    df['PLAIN_TEXT'] = df['PLAIN_TEXT'].apply(lambda x: re.sub(" +", " ", x))
    df['PLAIN_TEXT'] = df['PLAIN_TEXT'].str.replace('/', '', regex = False)
    df['PLAIN_TEXT'] = df['PLAIN_TEXT'].str.replace('*', '', regex = False)
    df['PLAIN_TEXT'] = df['PLAIN_TEXT'].apply(lambda x: x.replace('\'', ''))

    def replace_unicode_escapes(text):
        return re.sub(r'\\u[0-9a-fA-F]{4}', lambda m: chr(int(m.group(0)[2:], 16)), text)

    def remove_quotes_and_backslashes(text):
        return text.replace('\\', '').replace('"', '').replace("'", '')

    df['PLAIN_TEXT'] = df['PLAIN_TEXT'].apply(replace_unicode_escapes)
    df['PLAIN_TEXT'] = df['PLAIN_TEXT'].apply(remove_quotes_and_backslashes)
    df['PLAIN_TEXT'] = df['PLAIN_TEXT'].str.replace('\\', '', regex = False)

    df['URL'] = df['URL'].str.replace('\\', '', regex=False)

    df = df[df['PLAIN_TEXT'] != ""]

    df.to_json('reddit_articles.json', orient='records')


if __name__ == "__main__":
    main()

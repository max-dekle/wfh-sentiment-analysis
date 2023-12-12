import requests
import json
import pandas as pd
import re
from unidecode import unidecode
import datetime
<<<<<<< Updated upstream:data_deliverable/code/clean_nyt.py
import time
=======
from bs4 import BeautifulSoup
>>>>>>> Stashed changes:clean_nyt.py

API_KEY = 'ROUxHvEwZzYUQYLlWYbYR8I9WMSAxa6O'
URL = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'


# set up the parameters
params = {
    'api-key': API_KEY,
    'q': 'remote work',
    'sort': 'relevance',
    'show-fields': 'body'
}

r = requests.get(URL, params=params)
data = r.json()
# get the total number of results
total_results = data['response']['meta']['hits']
sofar = 0
articles = []
#loop through the results
while sofar < 900 and sofar < total_results:
    time.sleep(6.0)
    r = requests.get(URL, params={**params, 'page': sofar // 10})
    data = r.json()
    for article in data['response']['docs']:
        articles.append({
            'ID': article['_id'],
            'URL': article['web_url'],
            'DATE': article['pub_date'],
            'PLAIN_TEXT': article['lead_paragraph'] + article['snippet'],
            'SOURCE': "New York Times"
            })
    sofar += 10

# Save the results to a JSON file
with open('nytimes_articles.json', 'w') as f:
    json.dump(articles, f)

df = pd.read_json('nytimes_articles.json')

df.info()
df['PLAIN_TEXT'] = df['PLAIN_TEXT'].apply(lambda x: re.sub('\n', '', x))
df['PLAIN_TEXT'] = df['PLAIN_TEXT'].apply(lambda x: re.sub('<.*?>', '', x))
df['PLAIN_TEXT'] = df['PLAIN_TEXT'].apply(lambda x: unidecode(str(x)))
df['PLAIN_TEXT'] = df['PLAIN_TEXT'].apply(lambda x: re.sub(" +", " ", x))
df['PLAIN_TEXT'] = df['PLAIN_TEXT'].str.replace('/', '', regex = False)
df['PLAIN_TEXT'] = df['PLAIN_TEXT'].apply(lambda x: x.replace('\'', ''))

def replace_unicode_escapes(text):
    return re.sub(r'\\u[0-9a-fA-F]{4}', lambda m: chr(int(m.group(0)[2:], 16)), text)

def remove_quotes_and_backslashes(text):
    return text.replace('\\', '').replace('"', '').replace("'", '')

df['PLAIN_TEXT'] = df['PLAIN_TEXT'].apply(replace_unicode_escapes)
df['PLAIN_TEXT'] = df['PLAIN_TEXT'].apply(remove_quotes_and_backslashes)
df['PLAIN_TEXT'] = df['PLAIN_TEXT'].str.replace('\\', '', regex = False)

df['DATE'] = pd.to_datetime(df['DATE'], unit='s').dt.strftime('%Y-%m-%d')

df.to_json('nytimes_articles.json', orient='records')

"""
url = "https://www.nytimes.com/2023/03/21/world/europe/russia-ukraine-war.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

article_body = soup.find("div", {"class": "css-53u6y8"})
body_text = ""

for paragraph in article_body.find_all("p"):
    body_text += paragraph.get_text()

print(body_text)
"""

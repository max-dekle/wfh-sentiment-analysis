import pandas as pd
import matplotlib.pyplot as plt

sent_path = 'analysis\data\combined_scored_sentiment_ratings.json'
art_path = 'data_deliverable\data_files\combined_articles.json'
sents = pd.read_json(sent_path)
arts = pd.read_json(art_path)

df = pd.merge(sents, arts, how= 'inner', on= 'ID').reset_index()
df = df[df['METHOD'] == 'roberta_average_sentence_sentiment_conf_scaled']
df['DATE'] = pd.to_datetime(df['DATE'])
redditdf = df.loc[(df['SOURCE'] == 'Reddit /r/experienceddevs') | (df['SOURCE'] == 'Reddit /r/cscareerquestions')]
articledf = df.loc[(df['SOURCE'] == 'The Guardian') | (df['SOURCE'] == 'New York Times')]
yearly_sentiment = df.groupby(pd.Grouper(key='DATE', freq='Y'))['RATING'].mean().reset_index()
reddit_sentiment = redditdf.groupby(pd.Grouper(key='DATE', freq='Y'))['RATING'].mean().reset_index()
article_sentiment = articledf.groupby(pd.Grouper(key='DATE', freq='Y'))['RATING'].mean().reset_index()
# Yearly plot
plt.figure(figsize=(10,5))
x = list(yearly_sentiment['DATE'].dt.year)
plt.bar(yearly_sentiment['DATE'].dt.year - .2, yearly_sentiment['RATING'], width= .3, label='Aggregate')
plt.bar(reddit_sentiment['DATE'].dt.year, reddit_sentiment['RATING'], width= .3, label='Reddit')
plt.bar(article_sentiment['DATE'].dt.year + .2, article_sentiment['RATING'], width= .3, label='Magazines')
plt.title('Yearly Sentiment Ratings')
plt.xlabel('Year')
plt.ylabel('Sentiment Rating')
plt.xticks(x, x)
plt.legend()
plt.show()

monthly_sentiment = df.groupby(df['DATE'].dt.to_period('M'))['RATING'].mean()
reddit_sentiment = redditdf.groupby(df['DATE'].dt.to_period('M'))['RATING'].mean()
article_sentiment = articledf.groupby(df['DATE'].dt.to_period('M'))['RATING'].mean()
# Monthly plot
monthly_sentiment.plot(label='Aggregate')
reddit_sentiment.plot(label='Reddit')
article_sentiment.plot(label='Magazines')
plt.xlabel('Month')
plt.ylabel('Sentiment Rating')
plt.title('Monthly Sentiment Ratings (2020-2023)')
plt.legend()
plt.show()

# Calculate rolling mean of sentiment ratings with a 3-month window
sorted = df.sort_values(by= 'DATE')
#print(sorted.head())
rolling_sentiment = sorted.set_index('DATE')['RATING'].rolling('90D').mean()

# Create a line plot of rolling sentiment ratings
plt.plot(sorted['DATE'], sorted['RATING'], label='Raw Data')
plt.plot(rolling_sentiment.index, rolling_sentiment.values, label='Rolling Mean')
plt.xlabel('Date')
plt.ylabel('Sentiment Rating')
plt.title('Rolling Mean Sentiment Ratings (3-Month Window)')
plt.legend()
plt.show()

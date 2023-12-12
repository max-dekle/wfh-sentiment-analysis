import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

def two_sample_ttest(values_a, values_b):
    # TODO: Use scipy's ttest_ind
    # (https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html)
    # to get the t-statistic and the p-value. You can use the default fields (e.g., nan_policy)
    tstats, pvalue = ttest_ind(values_a, values_b)
    # TODO: You can print out the tstats, pvalue, and other necessary
    # calculations to determine your answer to the questions
    print("tstats: ", tstats)
    print("pvalue: ", pvalue)

    # and then we'll return tstats and pvalue
    return tstats, pvalue

combined_sentiment_path = '../data/combined_scored_sentiment_ratings.json'
sentiments = pd.read_json(combined_sentiment_path)

combined_articles_path = '../../data_deliverable/data_files/combined_articles.json'

articles = pd.read_json(combined_articles_path)

df = pd.merge(sentiments, articles, how= 'inner', on= 'ID').reset_index()

df = df[df['METHOD'] == 'roberta_average_sentence_sentiment_conf_scaled']

reddit_df = df[(df['SOURCE'] != 'The Guardian') & (df['SOURCE'] != 'New York Times')]
articles_df = df[(df['SOURCE'] == 'The Guardian') | (df['SOURCE'] == 'New York Times')]

print(' ')
print("2 Sample T-Test: Reddit Sentiments vs. Article (NYT & The Guardian) Sentiments" )

tstats, pvalue = two_sample_ttest(reddit_df['RATING'], articles_df['RATING'])

guardian_df = df[(df['SOURCE'] == 'The Guardian')]
nyt_df = df[(df['SOURCE'] == 'New York Times')]

print(' ')
print("2 Sample T-Test: The Guardian Sentiments vs. NYT Sentiments" )

tstats, pvalue = two_sample_ttest(guardian_df['RATING'], nyt_df['RATING'])

experienceddevs_df = reddit_df[(reddit_df['SOURCE'] == 'Reddit /r/experienceddevs')]
cscareerquestions_df = reddit_df[(reddit_df['SOURCE'] == 'Reddit /r/cscareerquestions')]

print(' ')
print("2 Sample T-Test: Reddit ExperiencedDevs Subreddit Sentiments vs. csCareerQuestions Subreddit Sentiments" )

tstats, pvalue = two_sample_ttest(experienceddevs_df['RATING'], cscareerquestions_df['RATING'])
print(' ')
"""
Augment data with sentiment scores computed from https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest .
"""

import pandas as pd
from nltk.tokenize import sent_tokenize
from transformers import pipeline
import argparse
import os


# helper function to generate score for a given article
def score_row(row):
    # print(row['URL'])
    # return row
    sentences = sent_tokenize(row['PLAIN_TEXT'])
    # truncate sentences that are too long
    def truncate_sent(x):
        if len(x) > 514:
            print(f"Found sentence too long: {x}")
            return x[:514]
        else:
            return x
    sentences = list(map(truncate_sent, sentences))
    # rating strategy: positive is +(confidence), negative is -(confidence), neutral is 0. Return average of sentence sentiments.
    sentiment_task = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest", tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest")
    sentence_sentiments = sentiment_task(sentences)

    def score_from_class(x):
        # helper to get scores from class
        if x['label'] == 'negative':
            return -x['score']
        elif x['label'] == 'positive':
            return x['score']
        elif x['label'] == 'neutral':
            return 0
    
    sentences_scores = list(map(score_from_class, sentence_sentiments))
    final_score = sum(sentences_scores) / len(sentences_scores)
    return pd.Series([row['ID'], 'roberta_average_sentence_sentiment_conf_scaled', final_score], index=['ID', 'METHOD', 'RATING'])

def main(orig_data_folder, output_folder):
    # load articles
    articles_df = pd.read_json(os.path.join(orig_data_folder, 'combined_articles.json'))

    # load existing sentiment ratings
    orig_sent_df = pd.read_json(os.path.join(orig_data_folder, 'combined_sentiment_ratings.json'))

    new_scores = articles_df.apply(score_row, axis=1)
    print(new_scores)
    new_sent_df = pd.concat([orig_sent_df, new_scores])
    # output to new dir
    new_sent_df.to_json(os.path.join(output_folder, 'combined_scored_sentiment_ratings.json'), orient='records')
    # integrity check: we scored everything once and didn't lose any rows
    assert len(new_sent_df) == len(articles_df) + len(orig_sent_df)

if __name__ == "__main__":
    a = argparse.ArgumentParser()
    # defaults are based on running script from project root
    a.add_argument("--orig_data_folder", type=str, default="data_deliverable/data_files/")
    a.add_argument("--output_folder", type=str, default="analysis/data/")
    args = a.parse_args()
    main(args.orig_data_folder, args.output_folder)
"""
We don't have ground-truth labels for the sentiment rating algorithm, so we need some other way to validate it.
To do this, we will take two approaches:
1. Automated validation against https://huggingface.co/datasets/financial_phrasebank 's dataset; this is a dataset
consisting of sentences extracted from (financial) news articles and given sentiment ratings of positive, negative, or neutral; this is the
same as the task we use our rating model for. This should give us a good signal of how accurate our model is on news articles.
2. Manual validation of a random sample of 20 articles, the results of which will be reported in our report.
"""
from datasets import load_dataset
from transformers import pipeline
import evaluate 
import pandas as pd
from argparse import ArgumentParser

def postprocess_results(x):
    # postprocess results dict to match format expected by financial phrasebank
    if x['label'] == 'negative':
        return 0
    elif x['label'] == 'positive':
        return 2
    elif x['label'] == 'neutral':
        return 1

def main(auto, manual):
    if manual:
        # gen a sample for manual validation

        articles_df = pd.read_json("data_deliverable/data_files/combined_articles.json")
        ratings_df = pd.read_json("analysis/data/combined_scored_sentiment_ratings.json")
        ratings_df = ratings_df[ratings_df['METHOD'] == 'roberta_average_sentence_sentiment_conf_scaled']

        for _, a in articles_df.sample(n=20).iterrows():
            rating = ratings_df[ratings_df['ID'] == a['ID']]
            print(f"RATING: {rating['RATING'].values[0]}")
            print(f"SOURCE: {a['SOURCE']}")
            print(f"TEXT: {a['PLAIN_TEXT']}")
            print()



    if auto:
        # run automatic validation and print results
        dataset = load_dataset("financial_phrasebank", 'sentences_allagree', split='train')

        acc_met = evaluate.load("accuracy", average=None)
        p_met = evaluate.load("precision", average=None)
        rec_met = evaluate.load("recall", average=None)
        f1_met = evaluate.load("f1", average=None)

        sentiment_task = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest", tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest")
        sentences = [dataset[i]['sentence'] for i in range(len(dataset))]
        sentence_sentiments = sentiment_task(sentences)

        preds = list(map(postprocess_results, sentence_sentiments))
        refs = [dataset[i]['label'] for i in range(len(dataset))]
    
        print(f"ACCURACY: {acc_met.compute(predictions = preds, references = refs)}")
        print(f"PRECISION: {p_met.compute(predictions = preds, references = refs, average=None)}")
        print(f"RECALL: {rec_met.compute(predictions = preds, references = refs, average=None)}")
        print(f"F1: {f1_met.compute(predictions = preds, references = refs, average=None)}")


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("--auto", action='store_true', default=False)
    p.add_argument("--manual", action='store_true', default=False)
    args = p.parse_args()
    main(args.auto, args.manual)

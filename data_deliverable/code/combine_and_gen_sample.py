import pandas as pd
from datetime import date


def main():
    # load everything up 
    guardian_a_df = pd.read_json("guardian_articles.json")
    reddit_a_df = pd.read_json("reddit_articles.json")
    nytimes_a_df = pd.read_json("nytimes_articles.json")
    # there is still a couple duplicates, drop them
    nytimes_a_df = nytimes_a_df.drop_duplicates(subset='PLAIN_TEXT', keep="first")
    guardian_a_df = guardian_a_df.drop_duplicates(subset='PLAIN_TEXT', keep="first")

    # convert nyt dates to datestamps



    reddit_sent_df = pd.read_json("reddit_sentiment_ratings.json")

    

    # create combined df
    combined_articles_df = pd.concat([guardian_a_df, reddit_a_df, nytimes_a_df])

    # data integrity checks
    # first, no records were lost
    assert len(combined_articles_df) == (len(guardian_a_df) + len(reddit_a_df) + len(nytimes_a_df))


    # filter to being written at least after 2020
    combined_articles_df = combined_articles_df.loc[combined_articles_df['DATE'] >= pd.to_datetime(1577836800, unit='s')]
    combined_articles_df['DATE'] = pd.to_datetime(combined_articles_df['DATE'], unit='s').dt.strftime('%Y-%m-%d')

    text_group = guardian_a_df.groupby('PLAIN_TEXT')
    size = text_group.size()
    print(size[size > 1])    

    assert len(reddit_a_df) == reddit_a_df['PLAIN_TEXT'].nunique(), f"{len(reddit_a_df)}, {reddit_a_df['PLAIN_TEXT'].nunique()}"
    assert len(nytimes_a_df) == nytimes_a_df['PLAIN_TEXT'].nunique()
    assert len(guardian_a_df) == guardian_a_df['PLAIN_TEXT'].nunique()

   
    text_group = combined_articles_df.groupby('PLAIN_TEXT')
    size = text_group.size()
    print(size[size > 1])
    # second, all items are unique
    # check for uniqueness by way of PLAIN_TEXT
    assert len(combined_articles_df) == combined_articles_df['PLAIN_TEXT'].nunique(), f"{len(combined_articles_df)}, {combined_articles_df['PLAIN_TEXT'].nunique()}"
    
    #and check that PKs are unique
    assert len(combined_articles_df) == combined_articles_df['ID'].nunique()

    # finally check that there are no nulls
    assert not combined_articles_df.isnull().values.any()

    # reddit sent is already guaranteed to be unique by construction
    # but we should check for nulls in case of a script error
    assert not reddit_sent_df.isnull().values.any()

    # currently only have sentiments for reddit - will generate more later during analysis
    reddit_sent_df.to_json('combined_sentiment_ratings.json', orient='records')
    combined_articles_df.to_json('combined_articles.json', orient='records')

    # generate sample
    sample_articles = combined_articles_df.sample(n=100)
    sample_sents = reddit_sent_df.loc[reddit_sent_df['ID'].isin(sample_articles['ID'])]

    sample_articles.to_json('articles_SAMPLE.json', orient='records')
    sample_sents.to_json('sentiment_ratings_SAMPLE.json', orient='records')

    # total articles
    print(len(combined_articles_df))



if __name__ == "__main__":
    main()

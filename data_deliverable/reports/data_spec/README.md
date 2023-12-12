# Reddit, NYTimes, Guardian Articles
ID: A unique identifier for each article. Ranging in length from 8 to 32 characters, each value is distinct from others. No default value. Can include alphanumeric characters as well as underscores and other special characters. We will double check in our analysis that each identifier is unique to ensure we don’t have duplicate records. This is a required value. We don’t think this contains sensitive information.

URL: A link to where the article is hosted on its respective source. A string containing alphanumeric as well as special characters. No default value. Each URL should be unique from other articles; we will check this in our analysis. We don’t think this contains sensitive information. We do not plan on using this as part of our main analysis, but rather as a sanity check to ensure distinct datapoints. 

DATE: A YYYY-MM-DD string representing the date in which the article was published. This does not have a default value. The range of values are from 2020-01-01 through 2023-03-22. The values are not guaranteed to be unique from one another since some articles were published at the same time even though they are distinct from one another. We will use this value as a metric in our analysis to determine how work-from-home sentiments have changed over the years. Required value. 

PLAIN_TEXT: The bulk of the data we will be using in our analysis. A long string of text that has been cleaned to contain only alphanumeric characters. Variable range and contents, but is related to the ‘remote work’ keyword. Words within the PLAIN_TEXT can be repeated but PLAIN_TEXTs should not be duplicates of other PLAIN_TEXTs. Required value. 

SOURCE: The source of the Article. Either Reddit /r/programming, Reddit /r/experienceddevs, Reddit /r/cscarreerquestions, The Guardian, or the New York Times. Required value, and the range is between these five values listed. No default value. 295 from the Guardian, 548 from Reddit, 307 from NYT. 

# Sentiment Rating
ID: Links back to the Article’s ID in the ‘Articles’ data. Required, not unique.

METHOD: Field detailing how the sentiment score was collected. Required, not unique, though pairs of (ID, METHOD) can be used to detect duplicate records.

RATING: The numeric (floating-point) rating of sentiment. Exact range depends on method; generally, higher numbers represent more positive sentiment. For example, reddit voting scores are in the range from 200 to over 10,000. Required, not unique. We plan to use these ratings for the final analysis to test our hypotheses on the opinions of remote work between different communities and at different points in time; for instance, this will allow us to test if the average sentiment of Reddit posts related to remote work are higher than that of Guardian articles, or alternatively to test if reddit scores on remote work posts from 2020 are higher than those from 2022.

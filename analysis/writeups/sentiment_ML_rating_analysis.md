# Machine Learning Method 1
## Supervised Learning for Sentiment Analysis

### Model Selection
For this machine learning requirement, we utilized a supervised machine learning method in order to generate sentiment ratings for each of the articles collected during the data deliverable phase. In particular, we used the pre-trained model `cardiffnlp/twitter-roberta-base-sentiment-latest`, developed by Louriero et al. [1] for use with the TweetEval sentiment analysis benchmark by Barbieri et al. [2, 3] and hosted on [Huggingface](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest). We chose this model over other popular supervised systems such as [distilbert for sentiment analysis](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english) for the following reasons:
1. It performs a three-valued sentiment analysis task, i.e. it can rate a piece of text as being positive, negative, or neutral. This is in contrast to many other sentiment analysis models that can only output two values, positive or negative. This allows our sentiment ratings to be much more granular and therefore hopefully more accurate, as this allows us to record when our articles have a neutral tone and reduces the likelihood that a neutral article is mistakenly classified as positive or negative.
2. This is a recent (c. 2022) model that was trained on more than 100 million tweets [1], including tweets from 2020 and 2021. This means that the model is capable of discerning sentiment from COVID-related language; for instance, the model correctly classifies the phrase "COVID cases are on the rise." as having negative sentiment. 
3. This model is sufficiently small to be used for our analysis without needing external computing power; classifying the articles that we collected took less than two hours on an M1 MacBook Air. 

### Analytic Method & Challenges
One key quirk of the Roberta-Base model is that it can only process strings up to 514 characters long. Thus, in most cases it would be impossible to give the model the entire text of a given article to analyze. Thus, we needed to develop an analytical method that could address the following challenges:
1. The score should rate an entire article despite not being able to give the entire article to the model at once;
2. The score should be scaled to article length, i.e. a short article and a long article should have comparable scores;
3. The score should factor in the model's confidence, e.g. a prediction of positive sentiment with low confidence should have a smaller effect than one with high confidence.

To overcome these challenges, we developed the following methodology to score each article:

First, to break the article into process-able chunks, we utilized [NLTK's sentence tokenizer](https://www.nltk.org/api/nltk.tokenize.html) to split the article into sentences, truncating especially long sentences to 514 characters if necessary. Each sentence was then fed to the Roberta-Base sentiment model, which returns a class of either "Positive", "Negative", or "Neutral" along with a confidence level from 0-1. We then recorded a score for each sentence, which was equal to either the confidence level if the class was positive, the negative of the confidence level if the class was negative, or 0 if the class was neutral. Finally, we then computed the article's rating as the article's average sentence score, i.e. a number in the range [-1.0, 1.0].
To store this information, we generated a new `sentiment_ratings` row for each article rating. These records can be found in `combined_scored_sentiment_ratings.json` in records where `METHOD == 'roberta_average_sentence_sentiment_conf_scaled'`, and the code for generating them can be found in `analysis/code/rate_sentiment.py`. 

### Validation
Because we used a pre-trained supervised model in this case and did not have ground truth sentiment labels for our data, we could not apply traditional cross-validation methods to ensure correct output for our model. Instead, we developed a validation method to fulfill this purpose and check for some potential weaknesses of our approach. Namely, we were concerned with two potential problems:
1. While the model we chose was trained on social media posts and we therefore had confidence in its ability to correctly rate reddit posts, we also used it to rate news articles. Before moving forward, we knew we should check that it could maintain its effectiveness on news articles.
2. In general, we wanted to ensure that the generated scores aligned with the general sentiment of the articles we found, and were not skewed towards any particular sentiment.

To address each of these concerns, we developed both automated and manual validation strategies, each of which allowed us to check the first and second concerns respectively. Code for both can be found in `analysis/code/validate_sentiment.py`.

#### Automated Validation
To perform automated validation, we first needed to locate a dataset that contained sentences from news articles with ground-truth sentiment labels to simulate the task of generating scores for our data. The most suitable dataset that we were able to locate was the Financial Phrasebank dataset [4] created by Malo et al. This dataset consists of sentences from financial news articles with three-valued sentiment labels provided by a group of human annotators. For validation, we used a split of the data that only contained sentences for which all annotators agreed on the label. We ran the Roberta-Base model on the dataset and recorded a testing accuracy of 0.71, along with the following precision, recall, and F1 scores for each class:

|           | Negative | Neutral | Positive |  Avg  |
|-----------|----------|---------|----------|-------|
| Precision | 0.89     | 0.69    | 0.86     | 0.81  |
| Recall    | 0.34     | 0.97    | 0.28     | 0.53  |
| F1        | 0.50     | 0.81    | 0.42     | 0.58  |

First, we should compare this performance to that of the model on the twitter dataset, i.e. Loureiro et al.'s results.
On the Twitter sentiment dataset, the authors report an average recall of 0.72 [1]. This is substantially higher than the average recall on this dataset of 0.53. However, it is important to note that this lower average recall is driven almost entirely by low recall on the negative and positive classes; in other words, the Roberta-Base model has a bias towards rating news sentences neutrally. This is unsuprising, as most news style guides encourage a much more neutral tone than is typical of social media. This result suggests that we can most trust the model's output on news articles if it identifies significant positive or negative sentiment, whereas neutral outputs may be false positives. 

#### Manual Validation
To manually validate the output of the model, we spent approximately one hour of total effort manually reviewing the output of the model on 50 articles. Of these, 26 were from news sites and 24 were from reddit. Naturally, due to the fact the scores are continuous, it is not possible to calculate a precise accuracy of our model based on this processes; instead, we qualitatively recorded how often we agreed with the general output of the model, e.g. we would agree with an output of 0.15 if the article seemed mildly positive in tone. The results of this are below:

ARTICLES REVIEWED
|        | Agree | Disagree | Pct Agree |
|--------|-------|----------|-----------|
| Reddit |  21   |     3    | 87.5%     |
| News   |  21   |     5    | 80.8%     |

As expected, we agreed with the Reddit ratings more often than we did the news article ratings. This aligns with the results from automated validation, though it is notable that the drop in agreement is not nearly as large as the drop in recall. This discrepancy is likely due to the effects of scale; a few misclassified sentences would only have a small effect on the overall score of a lengthy article. Additionally, misclassifications are more likely to be low confidence, making their impact even smaller with the methodology we developed above.

However, these topline numbers fail to capture some nuances in the nature of the agreement/disagreement. Generally, disagreements were matters of degree rather than kind; in fact, there was only one NYT article where the polarity was outright wrong - an article was given a rating of 0.34 when the article's text was simply a positive sentence followed by a negative sentence, which should have resulted in an overall neutral rating. In fact, NYT articles were the source of almost all of the disagreement from news sites, which we now believe is the result of a quirk of how the NYT API functions. Because the NYT is a subscription newspaper, they only offer short article snippets or summaries through their API rather than the full text of articles. These are typically only a few sentences long, which means there is a much smaller proportion of neutral sentences compared to positive or negative sentences in each collected article. The result of this is that articles from the NYT tend to have larger-magnitude scores than those from Reddit or the Guardian when the scores are not 0.  However, as NYT articles are a smaller component of our dataset and the polarities of their ratings are still generally correct, we do not believe that this effect will poison our later analysis.


### Conclusion
In summary, we chose a Roberta-Base derived language model fine-tuned on the TweetEval dataset [2, 3] by Loureiro et al. [1] for the purpose of generating sentiment ratings for each of our collected articles. This model was chosen over other systems due to its recency, ability to correctly classify covid-related information, and appropriateness to the task of classifying social media posts. We validated its performance by checking the accuracy of its outputs on a financial news dataset as well as manually reviewing 50 article ratings from our dataset. We found that while it had a decent average class accuracy of 71% and precision of 81%, it had a poor recall of 53% driven by a significant bias towards rating news statements as neutral. Despite this, however, our manual review found that we agreed with the model's rating of our articles about 84% of the time across all sources. Because of this we believe that the ratings we generated are accurate enough for the remainder of our analysis.

To be clear, however, this does leave significant room for improvement. Had we more time to iterate on this system, we would have experimented more with using separate models to score reddit and news articles respectively. Alternatively, had we access to more compute, we could have experimented with using multiple models to score each article and averaging their predictions.

Overall, we consider this portion of our analysis to be a success and a strong base for our later tests.




### Works Cited
1. D. Loureiro, F. Barbieri, L. Neves, L. E. Anke, and J. Camacho-Collados, TimeLMs: Diachronic Language Models from Twitter. 2022.
2. F. Barbieri, J. Camacho-Collados, L. Espinosa-Anke, and L. Neves, “TweetEval:Unified Benchmark and Comparative Evaluation for Tweet Classification,” 2020.
3. S. Rosenthal, N. Farra, and P. Nakov, “SemEval-2017 task 4: Sentiment analysis in Twitter,” in Proceedings of the 11th international workshop on semantic evaluation (SemEval-2017), 2017, pp. 502–518.
4. P. Malo, A. Sinha, P. Korhonen, J. Wallenius, and P. Takala, “Good debt or bad debt: Detecting semantic orientations in economic texts,” Journal of the Association for Information Science and Technology, vol. 65, 2014.


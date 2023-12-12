import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import json
from scipy import stats

# Load and preprocess data
sent_path = '..\\data\\combined_scored_sentiment_ratings.json'
art_path = '..\\..\\data_deliverable\\data_files\\combined_articles.json'
sents = pd.read_json(sent_path)
arts = pd.read_json(art_path)
df = pd.merge(sents, arts, how='inner', on='ID').reset_index()
df = df[df['METHOD'] == 'roberta_average_sentence_sentiment_conf_scaled']
df['DATE'] = pd.to_datetime(df['DATE'])
df['WEEK'] = df['DATE'].dt.isocalendar().week
df['DATE'] = df['DATE'].dt.year.astype(str)
df = df[['ID', 'DATE', 'WEEK', 'RATING']]

# Define number of folds
k = 5

# Initialize lists to store scores
r2_scores = []
mse_scores = []

def split_by_week(year):
    scores = []
    for week in range(1, 53):
        year_val = str(year)
        next_year_val = str(int(year) + 1)
        week_val = np.uint32(week)
        sample = df[((df['DATE'] == year_val) | (df['DATE'] == next_year_val)) & (df['WEEK'] == week_val)]
        print("Sample #" + str(int((year - 2020) / 2) * 52 + week))
        print("Number of observations:" + str(len(sample)))
        print("Average sentiment: " + str(np.round(np.mean(sample['RATING']), 2)))
        scores.append((week, str(np.round(np.mean(sample['RATING']), 2))))
    if year == 2020:
        with open('train.json', 'w') as json_file:
            json.dump(scores, json_file)
    else:
        with open('test.json', 'w') as json_file:
            json.dump(scores, json_file)

split_by_week(2020)
split_by_week(2022)
train = pd.read_json('train.json')
test = pd.read_json('test.json')

# Rename columns for clarity
train.columns = ['Week', 'X']
test.columns = ['Week', 'Y']

# Merge the DataFrames on the Week column
merged_df = pd.merge(train, test, on='Week')

# Save the merged DataFrame to a JSON file
merged_df.to_json('merge.json', orient='records')

model = LinearRegression()
# X = merged_df['X'].values.reshape(-1, 1)
X = merged_df['X']
Y = merged_df['Y']

slope, intercept, r, p, std_err = stats.linregress(X, Y)
def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, X))

X = X.values.reshape(-1,1)
plt.scatter(X, Y)
plt.plot(X, mymodel)
plt.title("Sentiment Ratings Linear Regression Plot")
plt.xlabel("Ratings from 2020-2021 Articles")
plt.ylabel("Ratings from 2022-2023 Articles")
plt.savefig("Linear-Regression-Figure")

model.fit(X, Y)
r_sq = model.score(X, Y)
print(f"coefficient of determination: {r_sq}")
print(f"intercept: {model.intercept_}")
print(f"slope: {model.coef_}")
# Predict on test data
# y_pred = model.predict(X_test)

# # Evaluate the model
# mse = mean_squared_error(y_test, y_pred)
# r2 = r2_score(y_test, y_pred)

# print(f"Mean Squared Error: {mse}")
# print(f"R² Score: {r2}")

# #         train_df = df[(df['DATE'] == year) & (df['WEEK'] == week)]
# #         test_df = df[(df['DATE'].isin(['2022', '2023'])) & (df['WEEK'] == week)]
# #         # print("train_df.shape:", train_df.shape)
# #         # print("test_df.shape:", test_df.shape)

# #         if not train_df.empty and not test_df.empty:
# #             X_train = train_df[['RATING']]
# #             y_train = train_df[['RATING']]
# #             X_test = test_df[['RATING']]
# #             y_test = test_df[['RATING']]

# #             # Adjust the number of folds based on the sample size
# #             n_splits = min(k, len(X_train))
# #             if n_splits < 2:
# #                 # Skip this week if there are not enough samples for at least 2 splits
# #                 continue

# #             kf = KFold(n_splits=n_splits)

# #             for train_idx, test_idx in kf.split(X_train):
# #                 X_train_fold, X_test_fold = X_train.iloc[train_idx], X_train.iloc[test_idx]
# #                 y_train_fold, y_test_fold = y_train.iloc[train_idx], y_train.iloc[test_idx]

# #                 model = LinearRegression()
# #                 model.fit(X_train_fold, y_train_fold)

# #                 y_pred = model.predict(X_test_fold)
# #                 r2 = model.score(X_test_fold, y_test_fold)
# #                 mse = mean_squared_error(y_test_fold, y_pred)

# #                 r2_scores.append(r2)
# #                 mse_scores.append(mse)

# # # Calculate mean scores across all folds and weeks
# # mean_r2 = np.mean(r2_scores)
# # mean_mse = np.mean(mse_scores)

# # output = {
# #     "mean_r2": mean_r2,
# #     "mean_mse": mean_mse,
# # }

# # # Output results
# # print(f"Mean R^2: {mean_r2}")
# # print(f"Mean MSE: {mean_mse}")


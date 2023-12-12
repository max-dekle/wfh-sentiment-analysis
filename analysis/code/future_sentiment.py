import pandas as pd
import json
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.metrics import mean_squared_error

sent_path = '..\data\combined_scored_sentiment_ratings.json'
art_path = '..\..\data_deliverable\data_files\combined_articles.json'
sents = pd.read_json(sent_path)
arts = pd.read_json(art_path)

df = pd.merge(sents, arts, how= 'inner', on= 'ID').reset_index()
df = df[df['METHOD'] == 'roberta_average_sentence_sentiment_conf_scaled']

id_series = df['ID']
date_series = df['DATE']
rating_series = df['RATING']

## isolate ID, RATING, and DATE

df = pd.concat([id_series, date_series, rating_series], axis=1)

df['DATE'] = pd.to_datetime(df['DATE'])

df.to_json('sentiment_clean_data.json', orient='records')

# # Define your features (past sentiment scores) and target (future sentiment score)
x = df[df['DATE'].dt.year.isin([2020, 2021])]
x = x[2::]
x = x['RATING']
y = df[df['DATE'].dt.year.isin([2022, 2023])]
y = y['RATING']
x = x.to_numpy().reshape(-1,1)
y = y.to_numpy().reshape(-1,1)

print(f"X has {len(x)} records")
print(f"Y has {len(y)} records")

# define the parameter grid to search over
param_grid = {'fit_intercept': [True, False]}

# define the k-fold cross-validation object
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# define the grid search object
grid = GridSearchCV(LinearRegression(), param_grid=param_grid, scoring='r2', cv=kf)

# fit the grid search object to the data
grid.fit(x, y)

# print the best hyperparameters and resulting score
print(grid.best_params_)
print(grid.best_score_)

# fit the model with the best hyperparameters using all the data
model = grid.best_estimator_
model.fit(x, y)

# evaluate the model
r_sq = model.score(x, y)
intercept = model.intercept_
coef = model.coef_.tolist()
y_pred = model.predict(x).tolist()
mse = mean_squared_error(y, y_pred)

output = {
    "r_sq": r_sq,
    "intercept": intercept,
    "coef": coef,
    "mse": mse
}

with open('regression_output.json', 'w') as f:
    for key in output:
        f.write(f"{key}: {output[key]}\n")

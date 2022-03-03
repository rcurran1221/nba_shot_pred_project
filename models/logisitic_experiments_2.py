import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegressionCV
from sklearn.preprocessing import StandardScaler

shots_data = pd.read_csv('data/rob_data.csv')


features_to_use = ['shot_number', 'period', 'touch_time', 'shot_dist',
                   'close_def_dist',
                   # 'two_point_attempt',
                   'dribbles', 'pos_time_remaining', 'shot_success',
                   'action_type', 'shot_zone_area']

continuous_features = ['shot_number', 'period', 'touch_time', 'shot_dist',
                       'close_def_dist',
                       # 'two_point_attempt',
                       'dribbles', 'pos_time_remaining', 'shot_success']

scaler = StandardScaler().fit(shots_data[continuous_features])
shots_data[continuous_features] = scaler.transform(
    shots_data[continuous_features])
shots_data_subset = shots_data[features_to_use]
shots_data_subset = shots_data_subset.dropna().reset_index(drop=True)
X = shots_data_subset.drop(columns=['shot_success'])
X = pd.get_dummies(X)
y = shots_data_subset['shot_success'].astype(int)

logit = LogisticRegressionCV(
    cv=10, n_jobs=-1, max_iter=1000).fit(X, y)

max_score = 0
best_c = 0
for c, scores in enumerate(logit.scores_[1]):
    avg_score = sum(scores)/10
    if avg_score > max_score:
        max_score = avg_score
        best_c = logit.Cs_[c]

print(max_score)
print(best_c)
print(logit.intercept_)
coef_order = np.argsort(-abs(logit.coef_[0]))
for feature, coef in zip(X.columns[coef_order], logit.coef_[0][coef_order]):
    print(feature + ': ' + str(coef))

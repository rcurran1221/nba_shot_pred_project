import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
import pickle
import time

shots_data = pd.read_csv('../data/shot_log_location_plus.csv')

features_to_use = ['shot_number', 'period', 'touch_time', 'shot_dist',
                    'close_def_dist', 
                    'dribbles', 'pos_time_remaining','shot_success',
                    'action_type','shot_zone_area'] 

shots_data_subset = shots_data[features_to_use]
shots_data_subset = shots_data_subset.dropna().reset_index(drop=True)
X = shots_data_subset.drop(columns=['shot_success'])
X = pd.get_dummies(X)

y = shots_data_subset['shot_success'].astype(int)

start_time = time.time()
parameters =  {'n_estimators': [300, 400, 500], 'max_depth': [17] } # depth arrived at from other experiments not present here
random_forest = GridSearchCV(RandomForestClassifier(random_state=614), parameters, n_jobs = -1, verbose = 10, cv = 10).fit(X, y)
print(random_forest.best_params_) 
print(random_forest.best_score_)
feature_importances = random_forest.best_estimator_.feature_importances_
end_time = time.time()
print(end_time - start_time)

random_forest = random_forest.best_estimator_
feature_importances = random_forest.feature_importances_
feature_indexes = np.argsort(-feature_importances)
for name, importance in zip(X.columns[feature_indexes], feature_importances[feature_indexes]):
    print(name + ': ' + str(importance))
end_time = time.time()
print(end_time - start_time)

# pickle.dump(random_forest, open(filename, "wb"))
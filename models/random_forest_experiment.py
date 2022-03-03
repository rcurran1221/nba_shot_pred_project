import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
import pickle
import time

shots_data = pd.read_csv('data/rob_data.csv')

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
parameters =  {'n_estimators': [25], 'max_depth': [17] } # depth arrived at from other experiments not present here
random_forest = GridSearchCV(RandomForestClassifier(random_state=614), parameters, n_jobs = 1, verbose = 10, cv = 2).fit(X, y)
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


print(random_forest.estimators_)
trees = []

for forest_tree in random_forest.estimators_:
    samples = forest_tree.tree_.n_node_samples
    class1_positives = forest_tree.tree_.value[:,0,1]
    probs = (class1_positives/samples).tolist()

    trees.append(list(zip(forest_tree.tree_.__getstate__()['nodes'].tolist(), probs)))

with open("static/pickled_data/model_random_forest_classifier.pickle", "wb") as f:
    pickle.dump(trees, f, 0)

#############Now load in trees
data = X.loc[2,:].values
tree_outputs = []
for forest_tree in trees:
    node_pointer = 0
    while True:
        [left, right, feature, threshold, impurity, a, b], prob = forest_tree[node_pointer]
        if left == -1:
            tree_outputs.append(prob)
            break
        if data[feature] <= threshold:
            node_pointer = left
        else:
            node_pointer = right

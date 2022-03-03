import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import pickle
import matplotlib.pyplot as plt
import time


shots_data = pd.read_csv('data/rob_data.csv')


features_to_use = ['shot_number', 'period', 'touch_time', 'shot_dist',
                   'close_def_dist',
                   # 'two_point_attempt',
                   'dribbles', 'pos_time_remaining', 'shot_success']


# trees
shots_data_subset = shots_data[features_to_use]
shots_data_subset = shots_data_subset.dropna().reset_index(drop=True)
num_rows = shots_data_subset.shape[0]
sample = np.random.choice(num_rows, int(num_rows*0.8))
X = shots_data_subset.drop(columns=['shot_success'])
y = shots_data_subset['shot_success'].astype(int)

X_train = X.iloc[sample]
y_train = y.iloc[sample]

X_test = X.drop(sample)
y_test = y.drop(sample)
treeClf = tree.DecisionTreeClassifier().fit(X_train, y_train)

print(treeClf.score(X_test, y_test))

# 21000 leaves, probably too many...doesn't generalize well
# print(treeClf.get_n_leaves())

# we can also use "predict_proba" to arrive at a probabilistic outcome
print(treeClf.predict_proba(X_test))  # too many nodes so leafs are very pure

# max nodes = 100

treeClf = tree.DecisionTreeClassifier(max_leaf_nodes=100).fit(X_train, y_train)

print(treeClf.score(X_test, y_test))  # 62% accuracy with max leafs = 100

# print(treeClf.predict_proba(X_test))

treeClf = tree.DecisionTreeClassifier(max_leaf_nodes=10).fit(
    X_train, y_train)  # 61.7 % accuracy

print(treeClf.score(X_test, y_test))

# parameters = {'max_depth': [2, 4, 6, 8, 10]}
# treeGrid = GridSearchCV(tree.DecisionTreeClassifier(), parameters).fit(X, y)
#
# print(treeGrid.best_params_)
# print(treeGrid.best_score_)

features_to_use = ['shot_number', 'period', 'touch_time', 'shot_dist',
                   'close_def_dist',
                   # 'two_point_attempt',
                   'dribbles', 'pos_time_remaining', 'shot_success',
                   'action_type', 'shot_zone_area']

shots_data_subset = shots_data[features_to_use]
shots_data_subset = shots_data_subset.dropna().reset_index(drop=True)
num_rows = shots_data_subset.shape[0]
sample = np.random.choice(num_rows, int(num_rows*0.8))
X = shots_data_subset.drop(columns=['shot_success'])
X = pd.get_dummies(X)
y = shots_data_subset['shot_success'].astype(int)

# parameters = {'max_depth': [3]}
# simple_tree_grid = GridSearchCV(tree.DecisionTreeClassifier(),
#                                 parameters, n_jobs=1, cv=10).fit(X, y)
#
# print(simple_tree_grid.best_params_)
# print(simple_tree_grid.best_score_)

#tree.plot_tree(simple_tree_grid.best_estimator_, feature_names=X.columns)
#plt.show()

print(X.columns)

parameters = {'max_depth': [8]}
treeGrid = GridSearchCV(tree.DecisionTreeClassifier(),
                        parameters, n_jobs=1, cv=10).fit(X, y)

print(treeGrid.best_params_)
print(treeGrid.best_score_)

best_tree = treeGrid.best_estimator_


def get_feature_importances(tree_model):
    feature_importances = tree_model.feature_importances_
    feature_indexes = np.argsort(-feature_importances)
    for name, importance in zip(X.columns[feature_indexes], feature_importances[feature_indexes]):
        print(name + ': ' + str(importance))



get_feature_importances(best_tree)


samples = best_tree.tree_.n_node_samples
class1_positives = best_tree.tree_.value[:,0,1]
probs = (class1_positives/samples).tolist()


tree_object = list(zip(best_tree.tree_.__getstate__()['nodes'].tolist(), probs))

print(X["pos_time_remaining"].max())
print(X["pos_time_remaining"].min())
print(X["shot_number"].max())
print(X["shot_number"].min())

with open("static/pickled_data/model_tree_classifier.pickle", "wb") as f:
    pickle.dump(tree_object, f, 0)

d = X.loc[2,:].values
node_pointer = 0

while True:
    [left, right, feature, threshold, impurity, a, b], prob = tree_object[node_pointer]
    if left == -1:
        print(impurity, node_pointer, a, b, prob)
        break
    if d[feature] <= threshold:
        node_pointer = left
    else:
        node_pointer = right

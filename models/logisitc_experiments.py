import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import numpy as np
from matplotlib.pyplot import plot
from sklearn import tree
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

# reading data from csv
shots_data = pd.read_csv('../data/shots_log_location.csv')

# shots_data = sm.add_constant(shots_data) # need to add constant column manually when using statsmodels, constant column
# named 'const'

# converting all columns to lowercase for consistency, pandas columns are case
shots_data.columns = map(str.lower, shots_data.columns)
# sensative

shots_data['shot_success'] = (shots_data['shot_result'] == 'made').astype(
    int)  # converting to binary response

#print(np.sum((shots_data['close_def_dist'] == 0)))
#shots_data[(shots_data['close_def_dist'] == 0), 'close_def_dist'] = 0.01
#print(np.sum((shots_data['close_def_dist'] == 0)))

shots_data['inverse_def_dist'] = 1/shots_data['close_def_dist']

shots_data['two_point_attempt'] = (shots_data['pts_type'] == 2).astype(int)

logit_model_null = smf.logit('shot_success ~ 1', shots_data)
print(logit_model_null.fit().summary())

df = shots_data['shot_success'].value_counts()
success_prob = df.iloc[1] / (df.iloc[1] + df.iloc[0])
print(success_prob)

# shot_made_numeric has Nans ------------------------------------------------------
print(shots_data['shot_made_numeric'].head())  # sanity check of data
index = shots_data['shot_made_numeric'].index[shots_data['shot_made_numeric'].apply(
    np.isnan)]
# looks like some shot results in the shot_made_numeric are missing so using 'shot_result' instead
print(shots_data['shot_made_numeric'].isnull().values.any())
print(index)

#index = shots_data['shot_result'].index[shots_data['shot_result'].apply(str.isspace)]
# assert(len(index) == 0) # no missing values in this column

# print(shots_data['shot_success'])

# print(shots_data['close_def_dist'].head())
# print(shots_data['shot_dist'].head())

# basic logisitc model --------------------------

binomial_glm = smf.glm(formula='shot_made_numeric ~ close_def_dist + shot_dist',
                       data=shots_data, family=sm.families.Binomial())

binomial_glm_results = binomial_glm.fit()

print(binomial_glm_results.summary())

# binomial glm is the same model as the "logit" api, but "logit" provides a better output for comparing models with psuedo R squared measure

# shots_data['shot_made_numeric'] = shots_data['shot_made_numeric'].astype('int64')
#logit_model = smf.logit('shot_success ~ close_def_dist + shot_dist', shots_data)

#logit_model_results = logit_model.fit()

# print(logit_model_results.summary()) # this model is very bad, psuedoR2 of 0.03789***********

# logistic model with interaction term between defender and shot distance ----------------------------------

logit_model_interaction = smf.logit(
    'shot_success ~ close_def_dist:shot_dist', shots_data)

logit_model_interaction_results = logit_model_interaction.fit()

print(logit_model_interaction_results.summary())  # even worse, pR2 of 0.0087

# logistic model with interaction term and original features

logit_model_interaction_star = smf.logit(
    'shot_success ~ close_def_dist*shot_dist', shots_data)

logit_model_interaction_star_results = logit_model_interaction_star.fit()

# print(logit_model_interaction_star_results.summary()) # bad again, pR2 of 0.0418

# non linear models ----------------------------------------------------
# hypothesis: distance of defender has an exponential effect on shot outcome (closer to 0 is exponentially more impactful)

logic_non_linear = smf.logit(
    'shot_success ~ np.power(inverse_def_dist,2) + shot_dist', shots_data)

# print(logic_non_linear.fit().summary()) #bad again pR2 of 0.03

# add additional features ---------------------------------------------
# 2 vs 3 as categorical

shots_data['two_point_attempt'] = (shots_data['pts_type'] == 2).astype(int)

logit_2_pt = smf.logit(
    'shot_success ~ inverse_def_dist + shot_dist + two_point_attempt', shots_data)
model = logit_2_pt.fit().summary()
print(logit_2_pt.fit().summary())  # still bad


# https://planspace.org/20150423-forward_selection_with_statsmodels/
def forward_selected(data, response):
    """Linear model designed by forward selection.

    Parameters:
    -----------
    data : pandas DataFrame with all possible predictors and response

    response: string, name of response column in data

    Returns:
    --------
    model: an "optimal" fitted statsmodels linear model
           with an intercept
           selected by forward selection
           evaluated by adjusted R-squared
    """
    remaining = set(data.columns)
    remaining.remove(response)
    selected = []
    current_score, best_new_score = 0.0, 0.0
    while remaining and current_score == best_new_score:
        scores_with_candidates = []
        for candidate in remaining:
            formula = "{} ~ {} + 1".format(response,
                                           ' + '.join(selected + [candidate]))
            score = smf.logit(formula, data).fit().prsquared
            scores_with_candidates.append((score, candidate))
        scores_with_candidates.sort()
        best_new_score, best_candidate = scores_with_candidates.pop()
        if current_score < best_new_score:
            remaining.remove(best_candidate)
            selected.append(best_candidate)
            current_score = best_new_score
    formula = "{} ~ {} + 1".format(response,
                                   ' + '.join(selected))
    model = smf.logit(formula, data).fit()
    return model

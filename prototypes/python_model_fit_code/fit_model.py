import pandas as pd
from statsmodels.formula.api import logit
import pickle

#Note this code will only work in python 3 due to string encoding challenges with pickle

df = pd.read_csv("data/shot_logs.csv")
print(df.head())
df["SHOT_SUCCESS"] = (df["SHOT_RESULT"] == "made").astype(int)
print(df["SHOT_SUCCESS"])
m = logit('SHOT_SUCCESS ~ SHOT_DIST + CLOSE_DEF_DIST', df)
results = m.fit()
print(results.summary2())
print(results.predict({"SHOT_DIST": 5, "CLOSE_DEF_DIST": 1}))
print(results.predict({"SHOT_DIST": 5, "CLOSE_DEF_DIST": 5}))
with open("static/pickled_data/model_logistic_regression.pickle", "wb") as f:
    pickle.dump(dict(results.params), f, 0)

with open("static/pickled_data/model_logistic_regression.pickle", "r") as f:
    text = f.read()
    key = 'utf-8'
    pickle.loads(text.encode(key))

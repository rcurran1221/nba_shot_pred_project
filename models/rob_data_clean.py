import pandas as pd
import numpy as np

shots_data = pd.read_csv('data/shots_log_location.csv')

# shots_data = sm.add_constant(shots_data) # need to add constant column manually when using statsmodels, constant column
# named 'const'

# converting all columns to lowercase for consistency, pandas columns are case
shots_data.columns = map(str.lower, shots_data.columns)
# sensative 

shots_data['shot_success'] = (shots_data['shot_result'] == 'made').astype(
    int)  # converting to binary response

shots_data['two_point_attempt'] = (shots_data['pts_type'] == 2).astype(int)


def time_remaining(row):
    if pd.isna(row.shot_clock):
        return float(row.game_clock[-2:])
    else:
        return row.shot_clock

shots_data['pos_time_remaining'] = shots_data.apply(lambda row: time_remaining(row), axis = 1)

s# hots_data.to_csv(r'D:\CSE6242-Project\data\rob_data.csv')
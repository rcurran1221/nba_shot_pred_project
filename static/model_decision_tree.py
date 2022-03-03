let pythonCode_decisionTree = `
print("Runnign decision tree")
from js import window
import pickle
import numpy as np

shot_types = ["Alley Oop Dunk Shot","Alley Oop Layup shot","Driving Bank Hook Shot","Driving Bank shot","Driving Dunk Shot","Driving Finger Roll Layup Shot","Driving Hook Shot","Driving Jump shot","Driving Layup Shot","Driving Reverse Layup Shot","Driving Slam Dunk Shot","Dunk Shot","Fadeaway Bank shot","Fadeaway Jump Shot","Finger Roll Layup Shot","Floating Jump shot","Hook Bank Shot","Hook Shot","Jump Bank Hook Shot","Jump Bank Shot","Jump Hook Shot","Jump Shot","Layup Shot","Pullup Bank shot","Pullup Jump shot","Putback Dunk Shot","Putback Layup Shot","Putback Slam Dunk Shot","Reverse Dunk Shot","Reverse Layup Shot","Reverse Slam Dunk Shot","Running Bank Hook Shot","Running Bank shot","Running Dunk Shot","Running Finger Roll Layup Shot","Running Hook Shot","Running Jump Shot","Running Layup Shot","Running Reverse Layup Shot","Running Slam Dunk Shot","Running Tip Shot","Slam Dunk Shot","Step Back Jump shot","Tip Shot","Turnaround Bank Hook Shot","Turnaround Bank shot","Turnaround Fadeaway shot","Turnaround Hook Shot","Turnaround Jump Shot"]

shot_zones = ["Back Court(BC)","Center(C)","Left Side Center(LC)","Left Side(L)","Right Side Center(RC)","Right Side(R)"]

def dummy_shot_type(shot_type):
    return [1 if shot_type == x else 0 for x in shot_types]

def dummy_shot_zone(shot_zone):
    return [1 if shot_zone == x else 0 for x in shot_zones]


if 'model_object_tree' not in globals():
    model_object_tree = pickle.loads(window.parameters.model_object_tree.encode())
    return_string = "Drag nodes to estimate shot success"
    print(model_object_tree)

try:
    data = [
        window.parameters.SHOT_NUMBER,
        window.parameters.PERIOD,
        window.parameters.TOUCH_TIME,
        window.parameters.SHOT_DIST,
        window.parameters.CLOSE_DEF_DIST,
        window.parameters.DRIBBLES,
        window.parameters.POS_TIME_REMAINING] + dummy_shot_type(window.parameters.SHOT_TYPE) + dummy_shot_zone(window.parameters.SHOT_ZONE)#6
    node_pointer = 0
    print(data)
    while True:
        [left, right, feature, threshold, impurity, a, b], prob = model_object_tree[node_pointer]
        if left == -1:
            print(impurity, node_pointer, a, b)
            break
        if data[feature] <= threshold:
            node_pointer = left
        else:
            node_pointer = right
    print(prob)
    # Data order from robert's code
    # features_to_use = ['shot_number', 'period', 'touch_time', 'shot_dist',
    #                'close_def_dist', 'dribbles', 'pos_time_remaining','shot_success']

    return_string = "{:.2f}%".format(prob*100)
except Exception as e:
    print("Error", e)
return_string
`;

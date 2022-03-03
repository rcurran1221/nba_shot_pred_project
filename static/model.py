let pythonCode = `
from js import window
import pickle
import numpy as np
if 'model_object' not in globals():
    model_object = pickle.loads(window.parameters.model_object.encode())
    print("Model object loaded: ", model_object)
    return_string = "Drag nodes to estimate shot success"
try:
    #Placeholder calculation for probability
    log_odds = 0
    log_odds += model_object["SHOT_DIST"] * window.parameters.SHOT_DIST / 10
    log_odds += model_object["CLOSE_DEF_DIST"] * window.parameters.CLOSE_DEF_DIST / 10
    log_odds += model_object["Intercept"]
    return_string = "{:.2f}%".format(100/(1+np.exp(-log_odds)))
except Exception as e:
    print("Error", e)
return_string
`;

import numpy as np
import pandas as pd
from pycaret.time_series import *

def select_model(selection):
    models = {
    'Linear Regression': LinearRegression(),
    'K-Nearest Neighbors': KNeighborsRegressor(),
    'Random Forest': RandomForestRegressor(),
    'Gradient Boosting': GradientBoostingRegressor(),
    'XGBoost': XGBRegressor(verbosity = 0),
    'Support Vector Machines': LinearSVR(),
    'Extra Trees': ExtraTreesRegressor(),
     }
    
    return models[selection]




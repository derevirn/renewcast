import numpy as np
import pandas as pd
from pycaret.time_series import *
import logging
logging.disable(logging.CRITICAL)

def generate_forecast(df, select_model, forecast_horizon):
    ts = setup(df, fh = 144, verbose = False, numeric_imputation_target = 'linear')
    model = create_model(select_model, cross_validation = False)
    metrics = pull().drop('MAPE', axis = 1)
    model = finalize_model(model)
    prediction = predict_model(model, fh = forecast_horizon)
    prediction.set_index(prediction.index.to_timestamp(), inplace = True)
    col_name = df.columns[0] + ' Forecast'
    prediction.rename(columns = {'y_pred': col_name}, inplace = True)
    df = pd.concat([df, prediction])

    return df, metrics




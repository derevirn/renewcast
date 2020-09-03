import numpy as np
import pandas as pd
from sktime.forecasting.compose import ReducedRegressionForecaster
from sktime.utils.plotting.forecasting import plot_ys
from sklearn.linear_model import LinearRegression

def generate_forecast(df_, forecast_horizon = 24, window_length = 5):
    df = df_.copy()
    y_train = df.iloc[:,0].reset_index(drop=True)
    fh = np.arange(forecast_horizon) + 1
    regressor = LinearRegression()
    forecaster = ReducedRegressionForecaster(regressor=regressor, window_length=window_length,
                                             strategy='direct')
    forecaster.fit(y_train, fh=fh)
    y_pred = forecaster.predict(fh)
    
    
    date = df.index[0]
    periods = df.shape[0] + forecast_horizon
    date_index = pd.date_range(date, periods=periods, freq='H')
    col_name = df.columns[0] + ' Forecast' 
    df_pred = pd.DataFrame({col_name: y_pred}) 
    df = df.append(df_pred, ignore_index=True)
    df.set_index(date_index, inplace=True)
    return df
import numpy as np
import pandas as pd
from sktime.forecasting.compose import ReducedRegressionForecaster
from sktime.utils.plotting.forecasting import plot_ys
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import LinearSVR


def select_regressor(selection):
    regressors = {
    'Linear Regression': LinearRegression(),
    'K-Nearest Neighbors': KNeighborsRegressor(),
    'Random Forest': RandomForestRegressor(),
    'Gradient Boosting': GradientBoostingRegressor(),
    'Support Vector Machines': LinearSVR(),
    
     }
    return regressors[selection]



def generate_forecast(df_, regressor, forecast_horizon = 24, window_length = 5):
    df = df_.copy()
    y_train = df.iloc[:,0].reset_index(drop=True)
    fh = np.arange(forecast_horizon) + 1
    regressor = select_regressor(regressor)
    forecaster = ReducedRegressionForecaster(regressor=regressor, window_length=window_length,
                                             strategy='recursive')
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
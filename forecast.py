import numpy as np
import pandas as pd
from sktime.forecasting.compose import ReducedRegressionForecaster
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.performance_metrics.forecasting import smape_loss
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.svm import LinearSVR


def select_regressor(selection):
    regressors = {
    'Linear Regression': LinearRegression(),
    'K-Nearest Neighbors': KNeighborsRegressor(),
    'Random Forest': RandomForestRegressor(),
    'Gradient Boosting': GradientBoostingRegressor(),
    'Support Vector Machines': LinearSVR(),
    'Extra Trees': ExtraTreesRegressor(),
    
     }
    return regressors[selection]



def generate_forecast(df_, regressor, forecast_horizon, window_length):
    df = df_.copy()
    df.fillna(method = 'ffill', inplace = True)
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

def calculate_smape(df_, regressor, forecast_horizon, window_length):
    df = df_.copy()
    df.fillna(method = 'ffill', inplace = True)
    y = df.iloc[:,0].reset_index(drop=True)
    y_train, y_test = temporal_train_test_split(y, test_size = forecast_horizon)
    fh = np.arange(y_test.shape[0]) + 1
    regressor = select_regressor(regressor)
    forecaster = ReducedRegressionForecaster(regressor=regressor, window_length=window_length,
                                             strategy='recursive')
    forecaster.fit(y_train, fh=fh)
    y_pred = forecaster.predict(fh)
    
    return smape_loss(y_pred, y_test)
                                     
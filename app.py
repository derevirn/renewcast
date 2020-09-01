import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from country_mappings import COUNTRY_MAPPINGS
from credentials import get_token
from entsoe import EntsoePandasClient
from entsoe.mappings import TIMEZONE_MAPPINGS
from sktime.forecasting.compose import ReducedRegressionForecaster
from sktime.utils.plotting.forecasting import plot_ys
from sklearn.linear_model import LinearRegression


st.title("Forecasting Renewable Energy Production in EU")

country = st.selectbox(
    "Select a country code",
    list(COUNTRY_MAPPINGS.keys()))

country_code = COUNTRY_MAPPINGS[country]
client = EntsoePandasClient(api_key=get_token())

end = pd.Timestamp.now(tz=TIMEZONE_MAPPINGS[country_code]) - pd.DateOffset(days=1)
start = end - pd.DateOffset(days=60)

df = client.query_generation(country_code, start=start,end=end, psr_type=None)
df = df.resample('H').mean()
cols = ['Solar', 'Wind Onshore']

st.area_chart(df.iloc[720:][cols])

forecast_horizon = 72

wind_train = df['Wind Onshore'].reset_index(drop=True)
wind_fh = np.arange(forecast_horizon) + 1
regressor = LinearRegression()
forecaster = ReducedRegressionForecaster(regressor=regressor, window_length=5, strategy='direct')
forecaster.fit(wind_train, fh=wind_fh)
wind_pred = forecaster.predict(wind_fh)

solar_train = df['Solar'].reset_index(drop=True)
solar_fh = np.arange(forecast_horizon) + 1
regressor = LinearRegression()
forecaster = ReducedRegressionForecaster(regressor=regressor, window_length=5, strategy='direct')
forecaster.fit(solar_train, fh=solar_fh)
solar_pred = forecaster.predict(solar_fh)


date = df.index[0]
periods = df.shape[0] + forecast_horizon
date_index = pd.date_range(date, periods=periods, freq='H')
data = {'Wind Onshore Forecast': wind_pred,
        'Solar Forecast': solar_pred}
df_pred = pd.DataFrame(data)
df = df.append(df_pred, ignore_index=True)
df.set_index(date_index, inplace=True)


wind_cols = ['Wind Onshore', 'Wind Onshore Forecast']
solar_cols = ['Solar', 'Solar Forecast']

st.line_chart(df.iloc[720:][wind_cols])

st.line_chart(df.iloc[720:][solar_cols])
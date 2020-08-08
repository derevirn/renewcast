import streamlit as st
import pandas as pd
import numpy as np
import datetime
from country_mappings import COUNTRY_MAPPINGS
from credentials import get_token
from entsoe import EntsoePandasClient
from entsoe.mappings import TIMEZONE_MAPPINGS


st.title("Forecasting Renewable Energy Production in EU")

country = st.selectbox(
    "Select a country code",
    list(COUNTRY_MAPPINGS.keys()))

date_start = st.date_input(
    "Enter Start Date",
    datetime.date(2020,8,1))

date_end = st.date_input(
    "Enter End Date",
    datetime.date(2020,8,2))

country_code = COUNTRY_MAPPINGS[country]

client = EntsoePandasClient(api_key=get_token())
start = pd.Timestamp(date_start, tz=TIMEZONE_MAPPINGS[country_code])
end = pd.Timestamp(date_end, tz=TIMEZONE_MAPPINGS[country_code])
df = client.query_generation(country_code, start=start,end=end, psr_type=None)
df = df.resample('H').mean()
cols = ['Solar', 'Wind Onshore']

st.area_chart(df)

st.line_chart(df[cols])
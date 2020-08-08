import streamlit as st
import pandas as pd
import numpy as np
from country_mappings import COUNTRY_MAPPINGS
from credentials import get_token
from entsoe import EntsoePandasClient
from entsoe.mappings import TIMEZONE_MAPPINGS


st.title("Forecasting Renewable Energy Production in EU")

country = st.selectbox(
    "Select a country code",
    list(COUNTRY_MAPPINGS.keys()))

country_code = COUNTRY_MAPPINGS[country]

client = EntsoePandasClient(api_key=get_token())
start = pd.Timestamp('20200807', tz=TIMEZONE_MAPPINGS[country_code])
end = pd.Timestamp('20200808', tz=TIMEZONE_MAPPINGS[country_code])
df = client.query_generation(country_code, start=start,end=end, psr_type=None)
cols = ['Solar', 'Wind Onshore']

st.line_chart(df)
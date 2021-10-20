import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from entsoe import EntsoePandasClient #Install entsoe-py ver. 0.2.13 to ensure compatibility with the code.
from entsoe.mappings import TIMEZONE_MAPPINGS

#Using the caching mechanism of Streamlit,
#to download energy data from the ENTSOE API only when necessary
@st.cache
def get_energy_data(country_code):
    load_dotenv()
    token = os.environ['TOKEN']
    client = EntsoePandasClient(api_key=token)
    end = pd.Timestamp.now(tz=TIMEZONE_MAPPINGS[country_code])
    start = end - pd.DateOffset(months=1)
    df = client.query_generation(country_code, start=start,end=end, psr_type=None)
    #Resampling the dataframe with an hourly frequency,
    #because some of the countries provide time series
    #with higher frequencies (15T), but we don't need that.
    df = df.resample('H').mean()
    return df
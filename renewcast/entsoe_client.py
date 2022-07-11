from calendar import week
import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from entsoe import EntsoePandasClient
from entsoe.mappings import lookup_area

#Using the caching mechanism of Streamlit,
#to download energy data from the ENTSOE API only when necessary
@st.cache(ttl = 3600)
def get_energy_data(country_code):
    load_dotenv()
    token = os.environ['TOKEN']
    area = lookup_area(country_code)
    client = EntsoePandasClient(api_key=token)
    end = pd.Timestamp.now(tz=area.tz)
    start = end - pd.DateOffset(weeks=2)
    df = client.query_generation(area, start=start,end=end, nett = True, psr_type=None)
    df.set_index(df.index.tz_convert(None), inplace = True)
    #Resampling the dataframe with an hourly frequency,
    #because some of the countries provide time series
    #with higher frequencies (15T), but we don't need that.
    df = df.resample('H').mean()
    return df
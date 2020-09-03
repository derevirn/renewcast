import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from entsoe import EntsoePandasClient
from entsoe.mappings import TIMEZONE_MAPPINGS

@st.cache
def get_energy_data(country_code):
    load_dotenv()
    token = os.environ['TOKEN']
    client = EntsoePandasClient(api_key=token)
    end = pd.Timestamp.now(tz=TIMEZONE_MAPPINGS[country_code])
    start = end - pd.DateOffset(months=1)
    df = client.query_generation(country_code, start=start,end=end, psr_type=None)
    df = df.resample('H').mean()
    return df
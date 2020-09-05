import streamlit as st
from country_mappings import COUNTRY_MAPPINGS
from entsoe_client import get_energy_data
from forecast import generate_forecast, calculate_smape

st.title("Forecasting Renewable Energy Production in EU")
st.markdown("Select a country to view a chart of total renewable energy production,\
        as well as production forecasts for each type. You can also select the regression algorithm, \
        the forecast horizon, and the window length.")

country = st.sidebar.selectbox(label = "Select a Country", index = 9,
   options = list(COUNTRY_MAPPINGS.keys()))

regressor = st.sidebar.selectbox("Select a Regression Algorithm",
             ['Linear Regression', 'K-Nearest Neighbors', 'Random Forest',
              'Gradient Boosting', 'Support Vector Machines', 'Extra Trees' ])                    

st.subheader('Total Renewable Energy Production in ' + country + ' (MW)') 

forecast_horizon = st.sidebar.slider(label='Forecast Horizon (hours)',
                             min_value = 12, max_value = 168,
                             value = 48)

window_length = st.sidebar.slider(label = 'Window Length', min_value = 1,
                          value = 10)


country_code = COUNTRY_MAPPINGS[country]
df = get_energy_data(country_code)

cols_renewable = [ 'Wind Onshore', 'Wind Offshore', 'Solar', 'Biomass', 'Geothermal',
                   'Hydro Pumped Storage', 'Hydro Water Reservoir' ] 

df = df[df.columns & cols_renewable]

st.area_chart(df, use_container_width = False, width = 800)

for item in df.columns:
    
    smape = calculate_smape(df[[item]], regressor, forecast_horizon, window_length)
    st.subheader(item + ' Energy Production Forecast in ' + country + ' (MW)')
    
    df_forecast = generate_forecast(df[[item]], regressor, forecast_horizon, window_length)
    st.line_chart(df_forecast, use_container_width = False, width = 800)
    
    st.text('SMAPE: %.2f' % smape)
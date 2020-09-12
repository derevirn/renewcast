import streamlit as st
from country_mappings import COUNTRY_MAPPINGS
from entsoe_client import get_energy_data
from forecast import generate_forecast, calculate_smape

st.title("Renewcast: Forecasting Renewable Energy Generation in EU Countries")
st.markdown("Select a country to view the chart of total energy generation,\
        as well as forecasts for solar and wind energy. You can also select the regression algorithm, \
        the forecast horizon, and the window length (click/tap the arrow if you can't see the settings).\
        The SMAPE metric helps us estimate the accuracy of the forecast (lower is better). \
        Try adjusting the settings to lower the SMAPE value and get better results.\
        The Github repository of the app is available [here](https://github.com/derevirn/renewcast).\
        Feel free to contact me on [LinkedIn](https://www.linkedin.com/in/giannis-tolios-0020b067/)\
        or via [e-mail](mailto:derevirn@gmail.com).")

country = st.sidebar.selectbox(label = "Select a Country", index = 9,
                               options = list(COUNTRY_MAPPINGS.keys()))

regressor = st.sidebar.selectbox("Select a Regression Algorithm",   
                                 ['Linear Regression', 'K-Nearest Neighbors',
                                  'Random Forest', 'Gradient Boosting',
                                  'Support Vector Machines', 'Extra Trees' ])                    

st.subheader('Total Energy Generation in ' + country + ' (MW)') 

forecast_horizon = st.sidebar.slider(label = 'Forecast Horizon (hours)',
                                     min_value = 12, max_value = 168, value = 48)

window_length = st.sidebar.slider(label = 'Window Length',
                                  min_value = 1, value = 30)


country_code = COUNTRY_MAPPINGS[country]
df = get_energy_data(country_code)

#Plotting total energy generation for selected country
st.area_chart(df, use_container_width = False, width = 800)

cols_renewable = [ 'Wind Onshore', 'Wind Offshore', 'Solar'] 

#Selecting the renewable energy columns,
#Only if they are available in the dataframe
df = df[df.columns & cols_renewable]

for item in df.columns:
    
    smape = calculate_smape(df[[item]], regressor, forecast_horizon, window_length)
    st.subheader(item + ' Energy Generation Forecast in ' + country + ' (MW)')
    #Generating and plotting a forecast for each renewable energy type
    df_forecast = generate_forecast(df[[item]], regressor, forecast_horizon, window_length)
    st.line_chart(df_forecast, use_container_width = False, width = 800)
    st.text('SMAPE: %.2f' % smape)
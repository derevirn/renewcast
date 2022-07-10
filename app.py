import streamlit as st
from renewcast import *
#from entsoe_client import get_energy_data
#from renewcast.forecast import generate_forecast


st.set_page_config(page_title = "Renewcast ⚡")

st.title("Renewcast ⚡")
st.subheader('Forecasting Renewable Electricity Generation in EU Countries')

desc = '''Select a country to view the chart of total electricity generation,
        as well as forecasts for solar and wind energy. You can also select the forecasting model
        as well as the horizon of your preference (click the top left arrow if you can't see the settings).
        Try selecting a different model to decrease the forecasting error and get better results.
        The Github repository of the app is available [here](https://github.com/derevirn/renewcast).
        I encourage you to send your feedback via [e-mail](mailto:info@giannis.io) or follow me
        on [LinkedIn](https://www.linkedin.com/in/giannis-tolios-0020b067/).'''
st.markdown(desc)

country = st.sidebar.selectbox(label = "Select a Country", index = 9,
                               options = countries.keys())
                        
select_model = st.sidebar.selectbox("Select a Forecasting Model",   
                                 options = models.keys())                    

st.subheader('Total Electricity Generation in {} (MW)'.format(country)) 

forecast_horizon = st.sidebar.slider(label = 'Forecast Horizon (hours)',
                                     min_value = 12, max_value = 168, value = 48)


country_code = countries[country]
df = get_energy_data(country_code)

#Plotting total electricity generation for selected country
st.area_chart(df, use_container_width = False, width = 800)

cols_renewable = [ 'Wind Onshore', 'Wind Offshore', 'Solar'] 

#Selecting the renewable energy columns,
#Only if they are available in the dataframe
df = df[df.columns & cols_renewable]

for item in df.columns:
    
    st.subheader(item + ' Electricity Generation Forecast in ' + country + ' (MW)')
    #Generating and plotting a forecast for each renewable energy type
    df_forecast, metrics = generate_forecast(df[item].to_frame(), models[select_model], forecast_horizon)
    
    st.line_chart(df_forecast, use_container_width = False, width = 800)
    st.dataframe(metrics)

    print(df_forecast)

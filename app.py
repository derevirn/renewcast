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

#Creating the sidebar menu 
country = st.sidebar.selectbox(label = "Select a Country", index = 9,
                               options = countries.keys())

container_cat = st.sidebar.container()

               
select_model = st.sidebar.selectbox("Select a Forecasting Model",   
                                 options = models.keys())       
            

forecast_horizon = st.sidebar.slider(label = 'Forecast Horizon (hours)',
                                     min_value = 12, max_value = 168, value = 24)         

st.subheader('Total Electricity Generation in {} (MW)'.format(country)) 


#Getting the electricity data
country_code = countries[country]
df = get_energy_data(country_code)

#Plotting total electricity generation for selected country
st.area_chart(df, use_container_width = False, width = 800)
     

#Selecting the renewable energy columns
#that are available in the dataframe
cols_renewable = [ 'Wind Onshore', 'Wind Offshore', 'Solar'] 
df = df[df.columns & cols_renewable]
 
with container_cat:
        renewable_cat = st.selectbox(label = 'Select a Category', options = df.columns)   

st.subheader(renewable_cat + ' Electricity Generation Forecast in ' + country + ' (MW)')

#Generating and plotting a forecast for each renewable energy type
forecast_results = get_forecast_results(df[renewable_cat].to_frame(),
                   models[select_model], forecast_horizon)
                   
st.plotly_chart(forecast_results['forecast_fig'], use_container_width = False)
st.markdown('** Forecast result on test set and future values **')
st.dataframe(forecast_results['metrics'])


with st.expander('Display More Information'):
        st.plotly_chart(forecast_results['decomp_fig'], use_container_width = True)


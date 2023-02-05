import streamlit as st
import plotly.express as px
from renewcast import *

st.set_page_config(page_title = "Renewcast", page_icon="⚡")

with open( "style.css" ) as css: 
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.title("Renewcast ⚡")
st.markdown('#### Forecasting Renewable Electricity Generation in EU Countries')

desc = '''Select a country to view the total electricity generation plot,
        as well as forecasts for solar & wind energy. You can also specify the forecasting model
        and horizon of your preference (click the top left arrow if you can't see the settings).
        Try selecting a different model to decrease the forecasting error and get better results.
        Furthermore, I suggest using the app on a computer, as it has not been designed for smaller screens and 
        may have some issues on smartphones. Finally, you can check the app [Github repository](https://github.com/derevirn/renewcast)
        and send your feedback via [e-mail](mailto:info@giannis.io), or follow me on 
        [LinkedIn](https://www.linkedin.com/in/giannis-tolios-0020b067/) where I regularly post content.'''
st.markdown(desc)

#Creating the sidebar menu 
country = st.sidebar.selectbox(label = "Select a Country", index = 9,
                               options = countries.keys())

container_cat = st.sidebar.container()

select_model = st.sidebar.selectbox("Select a Forecasting Model",   
                                 options = models.keys())       

forecast_horizon = st.sidebar.slider(label = 'Forecast Horizon (hours)',
                                     min_value = 12, max_value = 168, value = 24)         

st.markdown('#### Total Electricity Generation in {} (MW)'.format(country)) 

#Getting the electricity data
country_code = countries[country]
df = get_energy_data(country_code)

#Plotting total electricity generation for selected country
#st.area_chart(df, use_container_width = True)
fig = px.area(df, x = df.index, y = df.columns, color_discrete_sequence=px.colors.qualitative.Prism)
fig.update_traces(line=dict(width=0.25))
fig.update_layout(height = 450, margin={"r":1,"t":10,"l":1,"b":1},
                  yaxis=dict(showgrid=False),
                  plot_bgcolor = '#FFFFFF', title = "",
                  legend = dict(orientation = 'h', title = ''),
                  yaxis_title='', xaxis_title='')

st.plotly_chart(fig, use_container_width = True)
     
#Selecting the renewable electricity columns that are available
cols_renewable = ['Wind Onshore', 'Wind Offshore', 'Solar'] 
df = df[df.columns & cols_renewable]
 
with container_cat:
        renewable_cat = st.selectbox(label = 'Select a Category', options = df.columns)   

st.markdown(f'#### {renewable_cat} Electricity Generation Forecast in {country} (MW)')

#Generating and plotting a forecast for the selected category
forecast_results = get_forecast_results(df[renewable_cat].to_frame(),
                   models[select_model], forecast_horizon)
                   
st.markdown('Result for test set and specified forecast horizon')                   
st.plotly_chart(forecast_results['forecast_fig'], use_container_width = True)
st.dataframe(forecast_results['metrics'].style.format(precision = 3))

with st.expander('Display More Plots'):
        st.markdown('#### Seasonal Decomposition Plot')
        st.plotly_chart(forecast_results['decomp_fig'], use_container_width = True)
        
        st.markdown('#### ACF Plot')
        st.plotly_chart(forecast_results['acf_fig'], use_container_width = True)

        st.markdown('#### Diagnostics Plot')
        st.plotly_chart(forecast_results['diag_fig'], use_container_width = True)
        
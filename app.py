import streamlit as st
import plotly.express as px
from renewcast import *

st.set_page_config(page_title = "Renewcast", page_icon="⚡")

with open( "style.css" ) as css: 
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.title("Renewcast ⚡")
st.markdown('### Forecasting Solar Electricity Generation in EU Countries')

desc = '''Select a country to view total electricity generation,
        as well as the solar electricity forecast. You can specify the forecasting model
        and horizon of your preference (click top arrow for settings).
        I suggest experimenting with different models to get more accurate results.
        You can click on **Display More Plots** for seasonal decomposition, ACF and forecast diagnostics.
        Furthermore, the data source is [ENTSO-E](https://www.entsoe.eu/) and all times are in **UTC**.
        You can check the app [Github repo](https://github.com/derevirn/renewcast)
        and send me your personal feedback via [e-mail](mailto:info@giannis.io). '''
st.markdown(desc)

#Creating the sidebar menu 
country = st.sidebar.selectbox(label = "Select a Country", index = 6,
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

with st.expander('Show Electricity Generation Dataset'):
        st.dataframe(df)
     
#Selecting the renewable electricity columns that are available
cols_renewable = ['Wind Onshore', 'Wind Offshore', 'Solar'] 
df = df[df.columns.intersection(cols_renewable)]

#with container_cat:
#        renewable_cat = st.selectbox(label = 'Select a Category', options = df.columns)   

st.markdown(f'#### Solar Electricity Generation Forecast in {country} (MW)')

#Generating and plotting a forecast for the selected category
forecast_results = get_forecast_results(df['Solar'].to_frame(),
                   models[select_model], forecast_horizon)
                   
st.markdown('Result for test set (previous 24h) and specified forecast horizon')                   
st.plotly_chart(forecast_results['forecast_fig'], use_container_width = True)
st.dataframe(forecast_results['metrics'].style.format(precision = 3))

with st.expander('Display More Plots'):
        st.markdown('#### Seasonal Decomposition Plot')
        st.plotly_chart(forecast_results['decomp_fig'], use_container_width = True)
        
        st.markdown('#### ACF Plot')
        st.plotly_chart(forecast_results['acf_fig'], use_container_width = True)

        if forecast_results['diag_fig'] != None:
                diag_fig = forecast_results['diag_fig']
                diag_fig.update_layout(height = 600,
                margin={"r":1,"t":19,"l":1,"b":1},
                plot_bgcolor = '#FFFFFF', title = '')

                st.markdown('#### Diagnostics Plot')
                st.plotly_chart(forecast_results['diag_fig'], use_container_width = True)
        

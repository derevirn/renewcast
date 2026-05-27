import numpy as np
import pandas as pd
import streamlit as st
from statsmodels.stats.descriptivestats import describe
from pycaret.time_series import *
import logging
logging.disable(logging.CRITICAL)

@st.cache_resource(max_entries=2)
def get_forecast_results(df, model_code, fh):

    test_len = 24 # test set equals 24 hours
    forecast_horizon = test_len + fh # user specified FH plus test set

    engine = None
    if model_code == 'auto_arima': engine = 'statsforecast'

    #Create forecasting model
    setup(df, fh = test_len, seasonal_period=24, 
          fold_strategy= 'expanding', verbose = False,
          numeric_imputation_target = 'linear')
    
    model = create_model(model_code, cross_validation = False, engine = engine)
    metrics = pull().drop('MAPE', axis = 1)
 
    #Create a Plotly figure for the forecast 
    fig_kwargs = {'renderer': 'plotly_mimetype'}
    data_kwargs = {'fh': forecast_horizon}

    forecast_fig = plot_model(model, 'forecast', return_fig = True,
                   fig_kwargs = fig_kwargs, data_kwargs = data_kwargs)
    forecast_fig.update_layout(height = 400,
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=False),
                    margin={"r":1,"t":15,"l":1,"b":1},
                    plot_bgcolor = '#FFFFFF',
                    legend = dict(orientation = 'h', yanchor = 'top'),
                    yaxis_title='', xaxis_title='',
                    title = "")

    #Create a Plotly figure with the decomposition plot
    decomp_fig = plot_model(plot = 'decomp', return_fig = True,
                 fig_kwargs = fig_kwargs, data_kwargs = data_kwargs)
    decomp_fig.update_layout(height = 600,
                    margin={"r":1,"t":18,"l":1,"b":1},
                    plot_bgcolor = '#FFFFFF',
                    title = '')

    #Create a Plotly figure with the ACF plot
    acf_fig = plot_model(plot = 'acf', return_fig = True,
                 fig_kwargs = fig_kwargs, data_kwargs = data_kwargs)
    acf_fig.update_layout(height = 400,
                    yaxis=dict(showgrid=False),
                    margin={"r":1,"t":18,"l":1,"b":1},
                    plot_bgcolor = '#FFFFFF',
                    title = '')

    #Create a Plotly figure with the diagnostics plot
    diagnostics_fig = plot_model(model, plot = 'diagnostics', return_fig= True,
                                fig_kwargs = fig_kwargs)

    forecast_dict = {
        'metrics': metrics,
        'forecast_fig': forecast_fig,
        'decomp_fig': decomp_fig,
        'acf_fig': acf_fig,
        'diag_fig': diagnostics_fig
    }

    return forecast_dict


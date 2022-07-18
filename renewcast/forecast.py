import numpy as np
import pandas as pd
import streamlit as st
from statsmodels.stats.descriptivestats import describe
from pycaret.time_series import *
import logging
logging.disable(logging.CRITICAL)

@st.cache(allow_output_mutation=True)
def get_forecast_results(df, model_code, forecast_horizon):

    engine = None
    if model_code == 'auto_arima': engine = 'statsforecast'

    #Create forecasting model
    ts = setup(df, fh = 24, verbose = False, numeric_imputation_target = 'linear')
    model = create_model(model_code, cross_validation = False, engine = engine)
    metrics = pull().drop('MAPE', axis = 1)
    '''
    model = finalize_model(model)
    prediction = predict_model(model, fh = forecast_horizon)
    prediction.set_index(prediction.index.to_timestamp(), inplace = True)
    col_name = df.columns[0] + ' Forecast'
    prediction.rename(columns = {'y_pred': col_name}, inplace = True)
    df = pd.concat([df, prediction])
    ''' 
    #Create a Plotly figure for the forecast 
    fig_kwargs = {'renderer': 'plotly_mimetype'}
    data_kwargs = {'fh': forecast_horizon + 24}

    forecast_fig = plot_model(model, 'forecast', return_fig = True,
                   fig_kwargs = fig_kwargs, data_kwargs = data_kwargs)
    forecast_fig.update_layout(height = 400,
                    margin={"r":1,"t":15,"l":1,"b":1},
                    plot_bgcolor = '#FFFFFF',
                    legend = dict(orientation = 'h', yanchor = 'top'),
                    yaxis_title='', xaxis_title='',
                    title = "")

    #Create a Plotly figure with the decomposition plot
    decomp_fig = plot_model(plot = 'decomp', return_fig = True,
                 fig_kwargs = fig_kwargs, data_kwargs = data_kwargs)
    decomp_fig.update_layout(height = 400,
                    margin={"r":1,"t":18,"l":1,"b":1},
                    plot_bgcolor = '#FFFFFF',
                    title = '')

    #Create a Plotly figure with the ACF plot
    acf_fig = plot_model(plot = 'acf', return_fig = True,
                 fig_kwargs = fig_kwargs, data_kwargs = data_kwargs)
    acf_fig.update_layout(height = 400,
                    margin={"r":1,"t":18,"l":1,"b":1},
                    plot_bgcolor = '#FFFFFF',
                    title = '')

    forecast_dict = {
        'metrics': metrics,
        'forecast_fig': forecast_fig,
        'decomp_fig': decomp_fig,
        'acf_fig': acf_fig
    }

    return forecast_dict


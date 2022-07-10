import numpy as np
import pandas as pd
from pycaret.time_series import *
import logging
logging.disable(logging.CRITICAL)

def get_forecast_results(df, select_model, forecast_horizon):

    #Create forecasting model
    ts = setup(df, fh = 36, verbose = False, numeric_imputation_target = 'linear')
    model = create_model(select_model, cross_validation = False)
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
    fig_kwargs = {'renderer': 'streamlit'}
    data_kwargs = {'fh': forecast_horizon + 36}

    forecast_fig = plot_model(model, 'forecast', return_fig = True,
                   fig_kwargs = fig_kwargs, data_kwargs = data_kwargs)
    forecast_fig.update_layout(width = 800, height = 400,
                    margin={"r":1,"t":15,"l":25,"b":1},
                    plot_bgcolor = '#FFFFFF',
                    title_text =" ")

    #Create a Plotly figure with the decomposition plot
    decomp_fig = plot_model(plot = 'decomp', return_fig = True,
                 fig_kwargs = fig_kwargs)
    decomp_fig.update_layout(width = 800, height = 400,
                    margin={"r":1,"t":18,"l":1,"b":1},
                    plot_bgcolor = '#FFFFFF',
                    title_text ='')

    forecast_dict = {
        'metrics': metrics,
        'forecast_fig': forecast_fig,
        'decomp_fig': decomp_fig,
    }

    return forecast_dict



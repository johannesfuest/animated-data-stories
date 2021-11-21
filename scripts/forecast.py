import pandas as pd
import numpy as np
from kats.consts import TimeSeriesData
from kats.models.prophet import ProphetModel, ProphetParams


def forecast_store_id(df_sales):
    store_type_id = 'ST04'

    # Let's aggregate e. g. the number of sales for each hierarchy1 level per day.
    df_global_sales_by_storetype = df_sales.groupby(
        by=['date', 'storetype_id'])['sales'].sum()

    # Get a slice for a specific hierachy level
    ts_sales_ST04 = df_global_sales_by_storetype.loc['2017-01-01':'2019-10-01', 'ST04']

    # TimeSeriesData requires
    ts_sales_ST04 = ts_sales_ST04.to_frame().reset_index()
    ts_sales_ST04.rename(
        columns={'date': 'time', 'sales': 'value'}, inplace=True)
    ts = TimeSeriesData(time=ts_sales_ST04.time, value=ts_sales_ST04.value)
    # create a model param instance
    # additive mode gives worse results
    params = ProphetParams(seasonality_mode='multiplicative')
    # create a prophet model instance
    m = ProphetModel(ts, params)
    # fit model simply by calling m.fit()
    m.fit()
    # make prediction for next 30 month
    fcst = m.predict(steps=30, freq="D")

    temp1 = fcst[['time', 'fcst']]
    temp1 = temp1.rename(columns={"fcst": "value"})
    temp2 = ts_sales_ST04[['time', 'value']]
    frames = [temp2, temp1]
    result = pd.concat(frames)
    result = temp1.rename(columns={"time": "date", "value": "sales"})

    res = {}
    res[store_type_id] = {}
    res[store_type_id]['threshold'] = pd.to_datetime(
        '2019-10-01', format='%Y-%m-%d')
    res[store_type_id]["data"] = result.to_numpy()
    res[store_type_id
        ]["text1"] = "Total number of products sold in stores of type 4 are predicted to dall by 20,7 % over the next 30 days."
    res[store_type_id
        ]["text2"] = "Consider counteracting this through advertising and check in with strategy planning to assess the situation."
    res[store_type_id]["y_label"] = "Daily units sold"
    res[store_type_id]["chart_type"] = 0
    return res

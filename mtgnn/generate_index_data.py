import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

import yfinance as yf
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
import matplotlib.pyplot as plt
import datetime as dt
from dateutil.relativedelta import relativedelta

def get_stock_data(start_date, end_date):
    nse30_path = 'data/nse30_historical.csv'
    stock_indices =['^MXX', '^JKSE', '^GSPTSE', '^FCHI', '^GDAXI', 'FTSEMIB.MI', '^N225', '^FTSE', '^GSPC', 'XU100.IS'] 

    data_indices = yf.download(stock_indices, start=start_date, end=end_date)
    data_indices = data_indices['2012-01-30':]

    nse30 = pd.read_csv(nse30_path)
    nse30.sort_index(ascending=False, inplace=True)
    nse30.index = pd.to_datetime(nse30['Date'])
    for i in range(0, len(nse30)):
        nse30['Open'].iloc[i] = locale.atof(nse30['Open'].iloc[i])

    idx = pd.date_range(
        data_indices.index[0].date(),
        data_indices.index[-1].date(),
    )
    data_indices.index = pd.DatetimeIndex(data_indices.index)
    data_indices = data_indices.reindex(idx, fill_value=np.nan).ffill()
    data_indices = data_indices.reindex(idx, fill_value=np.nan).bfill()
    nse30 = nse30.reindex(idx, fill_value=np.nan).ffill()
    nse30 = nse30.reindex(idx, fill_value=np.nan).bfill()

    data = data_indices['Open']
    data.insert(10, 'NSE30', nse30['Open'])

    for d in data['XU100.IS'].keys():
        if d.date() < dt.date(2020,7,27):
            data.at[d, 'XU100.IS'] = data.at[d, 'XU100.IS'] / 100

    data = data.map(lambda x: np.log(x))

    pd.DataFrame.to_csv(data.round(6), './data/indices.csv', index=False, header=False)
    return data
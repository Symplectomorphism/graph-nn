import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

import yfinance as yf
import numpy as np
import pandas as pd
# pd.options.mode.chained_assignment = None
import matplotlib.pyplot as plt
import datetime as dt
from dateutil.relativedelta import relativedelta

def get_stock_data(ticker, start_date, end_date):
    nse30_path = 'data/nse30.csv'
    stock_indices =['^MXX', '^JKSE', '^GSPTSE', '^FCHI', '^GDAXI', 'FTSEMIB.MI', '^N225', '^FTSE', '^GSPC', 'XU100.IS'] 
    data = yf.download(stock_indices, start=start_date, end=end_date)
    return data
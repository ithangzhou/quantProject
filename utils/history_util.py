from posixpath import split
from turtle import Turtle
from typing import Tuple
from gm.api import *
import os
import talib
import numpy as np
import pandas as pd
import requests

from pyecharts import options as opts
from pyecharts.charts import Kline

'''
history(symbol, frequency, start_time, end_time, fields=None, skip_suspended=True, 
        fill_missing=None, adjust=ADJUST_NONE, adjust_end_time='', df=True)
eg:
history_data = history(symbol='SHSE.000300', frequency='1d', start_time='2010-07-28',  end_time='2017-07-30', fields='open, close, low, high, eob,amount,volume', adjust=ADJUST_PREV, df= True)

'''
def gm_history(symbol, frequency, start_time, end_time, fields=None, skip_suspended=True, 
        fill_missing=None,df=True):
    return history(symbol=symbol,frequency=frequency,start_time=start_time
                   ,end_time=end_time,fields=fields,df=True)




if __name__ == '__main__':
    set_token('248ec0bf0d477b56513715b3a33825ba699036cc')
    res=gm_history('SHSE.600588','1d','2020-07-28','2022-07-30',fields='open, close, low, high, eob,amount,volume')
    price_data=res.iloc[:,0:4].values.tolist()
    x_axis=res['eob'].values.tolist()
    volumes=res['volume'].values.tolist()
    # print(res)
    c=(
        Kline()
        .add_xaxis(x_axis)
        .add_yaxis('Kline',price_data)
        .set_global_opts(yaxis_opts=opts.AxisOpts(is_scale=True)
                         ,xaxis_opts=opts.AxisOpts(is_scale=True)
                         ,title_opts=opts.TitleOpts(title='Kline_demo'))
        .render('kline_demo.html')
    )
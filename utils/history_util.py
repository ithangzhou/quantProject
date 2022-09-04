from posixpath import split
from turtle import Turtle
from typing import Tuple
from gm.api import *
import os
import talib
import numpy as np
import pandas as pd
# import requests
import talib as ta
import time

from pyecharts import options as opts
from pyecharts.charts import Kline,Line,Bar,Grid

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
    xaxis=[time.strftime('%Y-%m-%d',time.localtime(i//1000000000)) for i in x_axis]
    volumes=res['volume'].values.tolist()
    
    close_price=res.iloc[:,1]
    ma=talib.EMA(close_price,10).values.tolist()
    ma60=talib.EMA(close_price,60).values.tolist()
    # print(res)
    kline=(
        Kline()
        .add_xaxis(xaxis_data=xaxis)
        .add_yaxis('Kline',price_data)
        .set_global_opts(yaxis_opts=opts.AxisOpts(is_scale=True)
                         ,xaxis_opts=opts.AxisOpts(is_scale=True)
                         ,title_opts=opts.TitleOpts(title='Kline_demo'))
        # .render('kline_demo.html')
    )
    
    ma_line = (
     Line()
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
        .add_xaxis(xaxis_data=xaxis)
        .add_yaxis(
            series_name="",
            y_axis=ma,
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
    )    
    ma60_line = (
     Line()
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
        .add_xaxis(xaxis_data=xaxis)
        .add_yaxis(
            series_name="",
            y_axis=ma60,
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
    )
    overlap=kline.overlap(ma_line).overlap(ma60_line)
    (
        Grid()
        .add(
            overlap,
            grid_opts=opts.GridOpts(
                pos_top="20%",
                pos_left="10%",
                pos_right="10%",
                pos_bottom="15%",
                is_contain_label=True,
            ),
        )
        .render("ma_line_demo.html")
    )
    
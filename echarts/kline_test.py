from fileinput import close
from tracemalloc import start
from turtle import pos
from gm.api import *
from typing import Tuple
import os 
import talib as ta
import pandas as pd
import numpy as np
import time

from pyecharts import options as opts
from pyecharts.charts import Kline,Line,Bar,Grid

file_name = os.path.basename(__file__).split('.')[0]
out_file = "html/" + file_name + ".html" 
gm_token = '248ec0bf0d477b56513715b3a33825ba699036cc'
stock = 'SHSE.600588'
freq = '1d'
start_time='2020-07-28'
end_time='2022-07-30'
fields='open,close,low,high,eob,amount,volume'
short_gap=10
long_gap=60

def kline():
    set_token(gm_token)
    res=history(symbol=stock,frequency=freq,start_time=start_time,end_time=end_time,fields=fields,df=True)
    price=res.iloc[:,0:4].values.tolist()
    x_axis=res['eob'].values.tolist()
    xaxis=[time.strftime('%Y-%m-%d',time.localtime(i//1000000000)) for i in x_axis]
    volumes=res['volume'].values.tolist
    
    close_price=res.iloc[:,1]
    maShort=ta.EMA(close_price,short_gap).values.tolist()
    maLong=ta.EMA(close_price,long_gap).values.tolist()
    # macd, macdsignal, macdhist = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    macd, macdsignal, macdhist=ta.MACD(close_price,fastperiod=12,slowperiod=26,signalperiod=9)
    
    kline=(
        Kline()
        .add_xaxis(xaxis_data=xaxis)
        .add_yaxis('KLine_demo',price)
        .set_global_opts(yaxis_opts=opts.AxisOpts(is_scale=True)
                          ,xaxis_opts=opts.AxisOpts(is_scale=True)
                          ,title_opts=opts.TitleOpts(title='Kline_demo'))
    )
    
    ma_short = (
        Line()
        .add_xaxis(xaxis_data=xaxis)
        .add_yaxis(
            series_name="ma_short"
            ,y_axis=maShort
            ,symbol="maShot_line"
            ,is_symbol_show=True
            ,label_opts=opts.LabelOpts(is_show=True)
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True)
            ,xaxis_opts=opts.AxisOpts(type_='category')
            ,yaxis_opts=opts.AxisOpts(
                type_="value"
                ,axistick_opts=opts.AxisTickOpts(is_show=True)
                ,splitline_opts=opts.SplitLineOpts(is_show=True)
            )
        )
    )
    overlap=kline.overlap(ma_short)
    
    macd_line=(
        Line()
        .add_xaxis(xaxis_data=xaxis)
        .add_yaxis(series_name='macd'
                   ,y_axis=macd.values.tolist()
                   ,symbol='macd_short'
                   ,is_symbol_show=True
                   ,label_opts=opts.LabelOpts(is_show=True)
                   )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True)
        )
    )
    macd_line_long=(
        Line()
        .add_xaxis(xaxis_data=xaxis)
        .add_yaxis(series_name='macdLong'
                   ,y_axis=macdsignal.values.tolist()
                   ,symbol='macd_long'
                   ,is_symbol_show=True
                   ,label_opts=opts.LabelOpts(is_show=True)
                   )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True)
        )
    )
    macd_overlap=macd_line.overlap(macd_line_long)
    
    (
        Grid()
        .add(
            overlap
            ,grid_opts=opts.GridOpts(
                height='50%'
                ,pos_left='10%'
                ,pos_right='10%'
                ,is_contain_label=True
            )
        )
        .add(
            macd_overlap
            ,grid_opts=opts.GridOpts(
                height ='20%'
                ,pos_top="70%"
                ,pos_left='10%'
                ,pos_right='10%'
                ,is_contain_label=True
            )
        )
     .render(out_file)
     )
    



if __name__ == '__main__':
    kline()
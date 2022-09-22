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
short_gap=5
long_gap=20
ext_gap=60

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
    maExt=ta.EMA(close_price,ext_gap).values.tolist()
    # macd, macdsignal, macdhist = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    macd, macdsignal, macdhist=ta.MACD(close_price,fastperiod=12,slowperiod=26,signalperiod=9)
    
    kline=(
        Kline()
        .add_xaxis(xaxis_data=xaxis)
        .add_yaxis('KLine_demo',price)
        .add_yaxis(
            series_name='Kline'
            , y_axis=price
            , itemstyle_opts=opts.ItemStyleOpts(color='#ec0000',color0='#00da3c')
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(
                is_show=False,pos_bottom=10,pos_left="center"
            )
            ,datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False
                    , type_="inside"
                    ,xaxis_index=[0,1]
                    ,range_start=98
                    ,range_end=100
                )
                ,opts.DataZoomOpts(
                    is_show=True
                    ,xaxis_index=[0,1]
                    ,type_="slider"
                    ,pos_top="85%"
                    ,range_start=98
                    ,range_end=100
                )
            ]
            ,yaxis_opts=opts.AxisOpts(
                is_scale=True
                , splitarea_opts=opts.SplitAreaOpts(
                    is_show=True
                    , areastyle_opts=opts.AreaStyleOpts(opacity=1)
                )
            )
            , tooltip_opts=opts.TooltipOpts(
                trigger="axis"
                , axis_pointer_type="cross"
                , background_color="rgba(245,245,245,0.8)"
            )
            , visualmap_opts=opts.VisualMapOpts(
                is_show=False
                ,dimension=2
                ,series_index=5
                ,is_piecewise=True
                ,pieces=[
                    {"value": 1,"color": "#00da3c"}
                    ,{"value": -1,"color": "#ec0000"}
                ]
            )
            , axispointer_opts=opts.AxisPointerOpts(
                is_show=True
                ,link=[{"xAxisIndex": "all"}]
                ,label=opts.LabelOpts(background_color="#777")
            )
            ,brush_opts=opts.BrushOpts(
                x_axis_index="all"
                ,brush_link="all"
                ,out_of_brush={"color": 0.1}
                , brush_type="index"
            )
            )
    )
    
    ma = (
        Line()
        .add_xaxis(xaxis_data=xaxis)
        .add_yaxis(
            series_name="ma_short"
            ,y_axis=maShort
            ,symbol="maShot_line"
        )
        .add_yaxis(
            series_name="ma_long"
            ,y_axis=maLong
            ,symbol="maLong_line"
        )
        .add_yaxis(
            series_name="ma_ext"
            ,y_axis=maExt
            ,symbol="maExt_line"
        )
        # .set_global_opts(
        #     tooltip_opts=opts.TooltipOpts(is_show=True)
        #     ,xaxis_opts=opts.AxisOpts(type_='category')
        # )
    )
    overlap=kline.overlap(ma)
    
    macd_line=(
        Line()
        .add_xaxis(xaxis_data=xaxis)
        .add_yaxis(series_name='macd'
                   ,y_axis=macd.values.tolist()
                   ,symbol='macd_short'
                   )
        .add_yaxis(series_name='macdLong'
                   ,y_axis=macdsignal.values.tolist()
                   ,symbol='macd_long'
                   )
        .add_yaxis(series_name='bar'
                   ,y_axis=macdhist.values.tolist()
                   ,areastyle_opts=opts.AreaStyleOpts(opacity=1, color="#C67570")
                   )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True)
        )
    )
    
    (
        Grid()
        .add(
            overlap
            ,grid_opts=opts.GridOpts(
                height='50%'
                ,pos_left='10%'
                ,pos_right='10%'
                # ,is_contain_label=True
            )
        )
        .add(
            macd_line
            ,grid_opts=opts.GridOpts(
                height ='20%'
                ,pos_top="70%"
                ,pos_left='10%'
                ,pos_right='10%'
                # ,is_contain_label=True
            )
        )
     .render(out_file)
     )
    



if __name__ == '__main__':
    kline()
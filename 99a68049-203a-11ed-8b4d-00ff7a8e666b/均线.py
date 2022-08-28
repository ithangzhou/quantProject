# coding=utf-8
from __future__ import print_function,absolute_import
from email.mime import base
from symtable import Symbol
from gm.api import *
import os
import talib
import numpy as np

# 初始化参数
params={
    'token':'248ec0bf0d477b56513715b3a33825ba699036cc'
    ,'filename':__file__.split(os.sep)[-1]
    ,'start_time':'2019-04-01 09:30:00'
    ,'end_time':'2022-08-20 15:00:00'
    ,'init_cash':100000
}

# 上升趋势
def trendUp(arr):
    baseArr = arr[1:]
    sub = np.subtract(baseArr,arr[0:-1])
    if sub[-1] <= 0:
        return False
    for i in np.nditer(sub[-1:0:-1]):
        if i > 0:
            continue
        else:
            return True
    return True

# 上穿/下穿逻辑判断
def cross(arr1,arr2,upCross=True):
    sub = np.subtract(arr1,arr2)
    if upCross:
        if sub[-1] <= 0:
            return False
        
        for i in np.nditer(sub[-1:0:-1]):
            if i > 0:
                continue
            else:
                return True
        return True
    else:
        if sub[-1] > 0:
            return False
        
        for i in np.nditer(sub[-1:0:-1]):
            if i <= 0:
                continue
            else:
                return True
        return True

# 策略初始化
def init(context):
    context.tradeAmt=2000
    context.short=10
    context.long=20
    context.ll=60
    context.ss=5
    context.symbol='SHSE.600588'
    context.open_long=False
    context.open_short=False
    context.period=61
    context.buyed=0
    context.stopLossRate=0.10
    
      
    subscribe(context.symbol,frequency='1d',count=context.period)

# 事件处理
def on_bar(context,bars):
    data=context.data(symbol=context.symbol,frequency='1d',count=context.period,fields='close')
    
    closePrice=data.values
    
    maShort=talib.SMA(closePrice.reshape(context.period),context.short)
    maLong=talib.SMA(closePrice.reshape(context.period),context.long)
    maLL=talib.SMA(closePrice.reshape(context.period),context.ll)
    maSS=talib.SMA(closePrice.reshape(context.period),context.ss)
    pos=context.account().position(symbol=context.symbol,side=PositionSide_Long)
    
    macd, macdsignal, macdhist = talib.MACD(closePrice.reshape(context.period), fastperiod=context.short, slowperiod=context.long, signalperiod=9)
    
    if cross(maShort,maLong) and trendUp(maLL) and context.buyed == 0 and cross(macd,macdsignal) and trendUp(macd) and trendUp(maShort) and trendUp(maLong) and cross(maShort,maLL) and cross(maSS,maLong) and trendUp(macdsignal):
        if not pos:
            order_volume(symbol=context.symbol, volume=context.tradeAmt, side=OrderSide_Buy, order_type=OrderType_Limit, position_effect=PositionEffect_Open)
            context.buyed=1
            print('>>>>>>以市价单买入一手，买入价:[%f]' % (closePrice[-1]))
    elif pos and pos.price < pos.vwap*(1-context.stopLossRate) and context.buyed == 1:
        order_volume(symbol=context.symbol, volume=context.tradeAmt ,side=OrderSide_Sell, order_type=OrderType_Limit, position_effect=PositionEffect_Close)
        context.buyed=0
        print('<<<<<<<止损清仓！！，卖出价:[%f],浮动盈亏：[%f],盈亏比：[%f]' % (pos.price,pos.fpnl,pos.fpnl/pos.cost))
        
    elif pos and context.buyed == 1 and (cross(maShort,maLong,False) or cross(macd,macdsignal,False))  :
        order_volume(symbol=context.symbol, volume=context.tradeAmt ,side=OrderSide_Sell, order_type=OrderType_Limit, position_effect=PositionEffect_Close)
        context.buyed=0
        print('<<<<<<<以市价单卖出一手，卖出价:[%f],浮动盈亏：[%f],盈亏比：[%f]' % (pos.price,pos.fpnl,pos.fpnl/pos.cost))

            
if __name__== '__main__':
    run(strategy_id=params['filename'].split('.')[0]
        ,filename=params['filename']
        ,mode=MODE_BACKTEST
        ,token=params['token']
        ,backtest_start_time=params['start_time']
        ,backtest_end_time=params['end_time']
        ,backtest_adjust=ADJUST_PREV
        ,backtest_initial_cash=params['init_cash']
        ,backtest_commission_ratio=0.0001
        ,backtest_slippage_ratio=0.0001
    )
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
    # real = RSI(close, timeperiod=14)
    
  
            
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
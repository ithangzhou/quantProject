# coding=utf-8
import os
import sys
from gm.api import *


def init(context):
    schedule(schedule_func=algo,date_rule='1d',time_rule='14:50:00')


def algo(context):
    order_volume(symbol='SHSE.600000',volume=100,side=OrderSide_Buy,
    order_type=OrderType_Market,position_effect=PositionEffect_Open,price=0)
    
def on_back_test_finished(context,indicator):
    print(indicator)

if __name__ == '__main__':
    run(strategy_id='99a68049-203a-11ed-8b4d-00ff7a8e666b'
        , filename=os.path.basename(__file__)
        , mode=MODE_BACKTEST
        ,token='248ec0bf0d477b56513715b3a33825ba699036cc'
        , backtest_start_time='2022-01-01 00:00:00'
        , backtest_end_time='2022-06-14 15:00:00'
        , backtest_initial_cash=1000000
        , backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0.0001)

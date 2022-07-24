# coding=utf-8

import os
import sys
from gm.api import *


def init(context):
    # subscribe(symbols='SHSE.600000', frequency='1d')
    subscribe(symbols='SHSE.600000', frequency='30m')

def on_bar(context,bars):
    print(bars)


if __name__ == '__main__':
    run(strategy_id='9f1b9ccd-eb06-11ec-8163-00ff7a8e666b'
        , filename=os.path.basename(__file__)
    , mode=MODE_BACKTEST
    ,token='248ec0bf0d477b56513715b3a33825ba699036cc'
    ,backtest_start_time='2022-06-13 08:00:00'
    , backtest_end_time='2022-06-14 23:00:00'
    , backtest_adjust=ADJUST_PREV
    , backtest_initial_cash=10000000
    , backtest_commission_ratio=0.0001
    , backtest_slippage_ratio=0.0001)
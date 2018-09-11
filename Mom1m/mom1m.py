from rqalpha.api import *
import pickle
from datetime import datetime

def init(context):
    datas = pickle.load(open(r'HS300_datas_for_month_dict.pkl', 'rb'))
    context.datas = datas
    context.num = 10 # 买入/卖出最高/低的前n只


def before_trading(context):
    pass


def handle_bar(context, bar_dict):
    now_time=context.now.strftime("%Y-%m-%d")
    symbol_top = []
    symbol_bottom = []
    symbol_buy = []
    symbol_sell = []
    buy_count = 0
    sell_count = 0
    # 每月月初买入排名最高的10只股票，卖出排名最低的10只股票
    if now_time in context.datas.keys():
        for i in range(context.num):
            symbol_top.append(context.datas[now_time][i]['SYMBOL'])
            symbol_bottom.append(context.datas[now_time][-i]['SYMBOL'])
        for symbol in symbol_top:
            if symbol[0] == '6' :   # 沪A
                symbol = symbol + '.XSHG'
            else:                  # 0深A 3创业板
                symbol = symbol + '.XSHE'
            if not is_suspended(symbol):
                symbol_buy.append(symbol)
                buy_count=buy_count+1
        for symbol in symbol_bottom:
            if symbol[0] == '6' :   # 沪A
                symbol = symbol + '.XSHG'
            else:                  # 0深A 3创业板
                symbol = symbol + '.XSHE'
            if not is_suspended(symbol):
                symbol_sell.append(symbol)
                sell_count = sell_count+1
        # 先卖出
        for symbol in symbol_buy:
            order_target_value(symbol, 0)
        # 再买入
        cash = context.portfolio.cash
        buy_amount = cash / sell_count
        for symbol in symbol_sell:
            order_value(symbol, buy_amount)

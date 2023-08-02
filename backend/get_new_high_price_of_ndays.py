import sys
import datetime
import pandas as pd
import pdb
import time
import sqlite3
from pprint import pprint
import numpy as np
import akshare as ak
#import tushare as ts



def return_ndays(start_time, days, trade_date, activate=False):
    now = start_time
    #  now = datetime.datetime(2023, 7, 26, 15, 13, 56, 177376)
    print('now->', now)
    if activate:
        activate_start_time = datetime.datetime.strptime(
                str(datetime.datetime.now().date()) + '9:30', '%Y-%m-%d%H:%M'
                )
        activate_end_time = datetime.datetime.strptime(
                str(datetime.datetime.now().date()) + '15:00', '%Y-%m-%d%H:%M'
                )

        if activate_start_time <= now <= activate_end_time:
            current_day = (now - datetime.timedelta(1)).date()
        elif now < activate_start_time:
            current_day = (now - datetime.timedelta(1)).date()
        elif now > activate_end_time:
            current_day = now.date()
        else:
            current_day = now.date()
    else:
        current_day = now.date()


    if_exchage_day = trade_date[trade_date['trade_date']==current_day]
    if not if_exchage_day.empty:
        the_lastest_exchage_day = if_exchage_day.index[0]
        the_index_of_now = trade_date[trade_date['trade_date']==current_day].index[0]
    else:
        # 如果今天不是交易日, 那我们就往前倒， 直到是交易日为止
        i = 0
        while if_exchage_day.empty:
            i += 1
            current_day = current_day - datetime.timedelta(i)
            if_exchage_day = trade_date[trade_date['trade_date']==current_day]
        the_index_of_now = trade_date[trade_date['trade_date']==current_day].index[0]
    
    the_index_of_ndays = the_index_of_now - days
    if the_index_of_ndays < 0:
        sys.exit('error')
    else:
        recent_day = trade_date.iloc[the_index_of_ndays]['trade_date']
            

    print('current_day->', current_day)
    current_day_stf = current_day.strftime("%Y%m%d")
    print('last100day->', recent_day)
    recent_day_stf = recent_day.strftime('%Y%m%d')
    return {
        'start_day': recent_day_stf,
        'end_day': current_day_stf, 
    }





trade_date_hist_sina = ak.tool_trade_date_hist_sina()

stock_zh_list = ak.stock_zh_a_spot_em()
# stock_zh_codes = stock_zh_list['代码']

def get_max_price_of_codes(stock_zh_list, start_date, end_date):
    '''我想得到近5年的百日新高'''
    for index, line in stock_zh_list.iterrows():
        # breakpoint()
        start_time = datetime.datetime.now()
        print('index->', index, flush=True)
        print('start-time', start_time, flush=True)
        code = line['代码']
        name = line['名称']
        details_individual_info = ak.stock_individual_info_em(symbol=code)
        industry = details_individual_info.loc[details_individual_info.item == '行业', 'value'].to_list()[0]

        try:
            hist = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
        except:
            n = 2
            time.sleep(3)
            print(f"{n}次尝试", file=sys.stderr, flush=True)
            hist = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")

        if len(hist) <= 100:
            yield {
                "code": code, 
                "name": name,
                "select_start_date": datetime.datetime(1970,1,1),
                "select_end_date": datetime.datetime(1970,1,1), 
                "industry": industry, 
                "is_max_price_of_100days": False
                }
            continue
        for end in range(len(hist), 0, -1):
            start = end - 100
            select_start_date = hist.iloc[start]['日期']
            select_end_date = hist.iloc[end-1]['日期']
            current_price = hist.iloc[end-1]['收盘']
            window_of_hist = hist.iloc[start: end]['收盘']
            if len(window_of_hist) < 100:
                break
            max_price = window_of_hist.max()
            yield {
                "code": code, 
                "name": name,
                "select_start_date": select_start_date,
                "select_end_date": select_end_date, 
                "industry": industry, 
                "is_max_price_of_100days": current_price >= max_price
                }
        end_time = datetime.datetime.now()
        print('end-time', datetime.datetime.now(), flush=True)
        print('interval-of-start-and-end', end_time-start_time, flush=True)


# code = "603023"
# start_date = "20180104"
# end_date = "20230728"
# hist = ak.stock_zh_a_hist(symbol="603023", period="daily", start_date="20180104", end_date="20230728", adjust="qfq")

# start_date = hist.iloc[100]['日期']
# current_price = hist.iloc[100]['日期']
# max_price = hist.iloc[0: 100]['收盘'].max()
# current_price >= max_price

# dic = {"a": 1, "b": 2}
# dic1 = {'a': 3, "b": 4}
# df = pd.DataFrame([dic, dic1])
# con = sqlite3.connect('test.sqlite3')
# df.to_sql(con=con, name='aaa')

now = datetime.datetime.now()

# 暂时取了2年的数据， 500 + 100 = 600天
dates = return_ndays(now, 600, trade_date_hist_sina, True)

# create db
db = sqlite3.connect('./db/stock.sqlite3')
mem = []
for obj in get_max_price_of_codes(stock_zh_list, dates['start_day'], dates["end_day"]):
    mem.append(obj)

stocks = pd.DataFrame(mem)

stocks.to_sql(con=db, name='stocks', if_exists='append', index=True)
print('finished')




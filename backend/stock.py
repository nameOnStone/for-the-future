import datetime
import pandas as pd
import pdb
import time
import numpy as np
import akshare as ak
#import tushare as ts
#from pprint import pprint


def return_ndays(start_time, days, trade_date, activate=False):
    now = start_time
    #  now = datetime.datetime(2023, 7, 26, 15, 13, 56, 177376)
    print('now->', now, flush=True)
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
        last100day = trade_date.iloc[the_index_of_ndays]['trade_date']
            

    print('current_day->', current_day, flush=True)
    current_day_stf = current_day.strftime("%Y%m%d")
    print('last100day->', last100day, flush=True)
    last100day_stf = last100day.strftime('%Y%m%d')
    return {
        'today': current_day_stf, 
        'last100day': last100day_stf
    }


def lianzhang(series):
    list2 = series.tolist()
    list2.reverse()
    mem = []
    i = 0
    for ele in list2:
        if len(mem) == 0:
            mem.append(ele)
        elif len(mem) > 0:
            last = mem[-1]
            if ele < last:
                mem.append(ele)
            else:
                return i-1
        else:
            sys.exit(1)
        i += 1


def is_max_price_of_100days_in_the_stock(line):
    num = 1
    code = line['代码']
    name = line['名称']

    start_date = date_of_101days['last100day']
    end_date = date_of_101days['today']
    today = int(end_date)
    print('staring..', datetime.datetime.now(), flush=True)
    print(f'code={code}', flush=True)
    try:
        price_of_this_stock_101days = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
        details_individual_info = ak.stock_individual_info_em(symbol=code)
        industry = details_individual_info.loc[details_individual_info.item == '行业', 'value'].to_list()[0]
    except:
        time.sleep(10)
        num += 1
        print(f"开始{num}次执行此{code}票", flush=True)
        price_of_this_stock_101days = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
        details_individual_info = ak.stock_individual_info_em(symbol=code)
        industry = details_individual_info.loc[details_individual_info.item == '行业', 'value'].to_list()[0]

    #stock_individual_info_em_df = ak.stock_individual_info_em(symbol=code)
    print('ending...', datetime.datetime.now(), flush=True)
    # 这还没上市， 要特殊处理 和上市不足一年者， 应该去掉：
    # note: 不足一年，可能需要仔细定义。。我这里先简单为未不足365日
    
    price_of_this_stock_100days = price_of_this_stock_101days[1: 101] 


    # ST 股票去除 or 北京股市去除 or  特别的“科林退“（不懂这个退了为啥叫这个鬼名字）；
    if "ST" in name or code.startswith("83") or name == "科林退":
        return {
            'code': code, 
            'max_price_in_100days': 0, 
            'is_max_price_in_100days': False,
            'industry': industry,
            "how_far_from_max_price_of_100days": 0,
            "std_close_price_of_100days": 0,
            "days_of_lianzhang": 0,
            "is_still_new_max_price": "NN",
        }

    if details_individual_info.loc[details_individual_info['item']=="上市时间",'value'].tolist()[0] == "-" or \
        (today - details_individual_info.loc[details_individual_info['item']=="上市时间",'value'].tolist()[0]) <= 365:
        return {
            'code': code, 
            'max_price_in_100days': 0, 
            'is_max_price_in_100days': False,
            'industry': industry,
            "how_far_from_max_price_of_100days": 0,
            "std_close_price_of_100days": 0,
            "days_of_lianzhang": 0,
            "is_still_new_max_price": "NN",
        }

    if price_of_this_stock_100days.empty:
        return {
            'code': code, 
            'max_price_in_100days': 0, 
            'is_max_price_in_100days': False,
            'industry': industry,
            "how_far_from_max_price_of_100days": 0,
            "std_close_price_of_100days": 0,
            "days_of_lianzhang": 0,
            "is_still_new_max_price": "NN",
        }
        
    # max值只会有一个；
    max_price_of_100days_in_the_stock = max(price_of_this_stock_100days['收盘'])
    # 但是， max值的index却可能是多个， 我们最好给出距离今天最近的那一个, 其他的我们暂时不关心;
    the_index_of_max_price = price_of_this_stock_100days.loc[price_of_this_stock_100days['收盘']==max_price_of_100days_in_the_stock,'日期'].index[-1]
    the_index_of_lastest_days = price_of_this_stock_100days.tail(1).index[0]
    lastest_price_of_the_stock = price_of_this_stock_100days.tail(1)['收盘'].tolist()[0]
    
    # 相较昨天， 今天是否退出了百日新高? 那要首先知道昨天是不是新高
    
    price_of_this_stock_100days_yestoday = price_of_this_stock_101days[0: 100]
    max_price_of_100days_in_the_stock_yestoday = max(price_of_this_stock_100days_yestoday['收盘'])
    lastest_price_of_the_stock_yestoday = price_of_this_stock_100days_yestoday.tail(1)['收盘'].tolist()[0]
    is_max_price_in_100days_yestoday = lastest_price_of_the_stock_yestoday >= max_price_of_100days_in_the_stock_yestoday
    is_max_price_in_100days = lastest_price_of_the_stock >= max_price_of_100days_in_the_stock
    if (is_max_price_in_100days_yestoday == True) & (is_max_price_in_100days == True):
        is_still_new_max_price = "YY"
    elif (is_max_price_in_100days_yestoday == True) & (is_max_price_in_100days == False):
        is_still_new_max_price = "YN"
    elif (is_max_price_in_100days_yestoday == False) & (is_max_price_in_100days == True):
        is_still_new_max_price = "NY"
    elif (is_max_price_in_100days_yestoday == False) & (is_max_price_in_100days == False):
        is_still_new_max_price = "NN"
    else:
        sys.exit(1)



    
    how_far_days = the_index_of_lastest_days - the_index_of_max_price
    # if how_far_days == 99:
    #     pdb.set_trace()
    print('the_index_of_lastest_days - the_index_of_max_price->', how_far_days)
    #  floating_precentage_of_price_per_day = floating_precentage_of_price / (the_index_of_lastest_days - the_index_of_max_price)

    # 百日标准差
    close_price_of_100days = price_of_this_stock_100days['收盘']
    days_of_lianzhang = lianzhang(close_price_of_100days) + 1
    std_close_price_of_100days = close_price_of_100days.std(ddof=1)
    return {
        'code': code, 
        'max_price_in_100days': max_price_of_100days_in_the_stock, 
        'is_max_price_in_100days': is_max_price_in_100days,
        'industry': industry,
        "how_far_from_max_price_of_100days": how_far_days,
        "std_close_price_of_100days": std_close_price_of_100days,
        "days_of_lianzhang": days_of_lianzhang,
        "is_still_new_max_price": is_still_new_max_price,
    }



stock_zh_list = ak.stock_zh_a_spot_em()

#stock_zh_list = stock_zh_list.head(50)

trade_date_hist_sina = ak.tool_trade_date_hist_sina()
now = datetime.datetime.now()
#now = datetime.datetime(2023, 8, 14, 15, 13, 56, 177376)
date_of_101days = return_ndays(now, 100, trade_date_hist_sina, activate=True)


details_of_100days = stock_zh_list.apply(is_max_price_of_100days_in_the_stock, axis=1)


stock_zh_list['是否百日新高'] = pd.Series([obj['is_max_price_in_100days'] for obj in details_of_100days])
stock_zh_list['百日新高价格'] = pd.Series([obj['max_price_in_100days'] for obj in details_of_100days])
stock_zh_list['所属行业'] = pd.Series([obj['industry'] for obj in details_of_100days])
stock_zh_list['距百日新高有多少个交易日'] = pd.Series([obj['how_far_from_max_price_of_100days'] for obj in details_of_100days])
stock_zh_list['百日标准差'] = pd.Series([obj['std_close_price_of_100days'] for obj in details_of_100days])
stock_zh_list['连涨天数'] = pd.Series([obj['days_of_lianzhang'] for obj in details_of_100days])
stock_zh_list['昨日新高与今日新高'] = pd.Series([obj['is_still_new_max_price'] for obj in details_of_100days])
stock_zh_list['所属行业新高股票数'] = pd.Series([len(stock_zh_list[ (stock_zh_list['是否百日新高']==True) & (stock_zh_list['所属行业']==industry) ])  for industry in stock_zh_list['所属行业']])
#stock_zh_list.to_csv("stock_list.xls", sep='\t', encoding='gbk', index=False)
with pd.ExcelWriter(f"./db/stock_list.{date_of_101days['today']}.xlsx") as writer:
    stock_zh_list.to_excel(writer, sheet_name=f"{date_of_101days['today']}", index=False)
print('finished...', flush=True)

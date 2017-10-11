import gdax
import pandas as pd
import time
from datetime import datetime, timedelta
import os
import pytz

# initiate public client
public_client = gdax.PublicClient()


# determine if a date is summer time
def is_summer_time(aware_dt):
    assert aware_dt.tzinfo is not None
    assert aware_dt.tzinfo.utcoffset(aware_dt) is not None
    return bool(aware_dt.dst())


# try to get one feed request, if succeed, append feed to data list and return True, if fail return False
def try_get_feed(ticker, start, end, hist_data, granularity=1):
    try:
        feed = public_client.get_product_historic_rates(ticker, start, end, granularity)
        if len(feed) == 0:
            print('empty record, get next feed...')
            return True
        if feed[0] != 'message':
            for record in reversed(feed):
                record[0] = datetime.fromtimestamp(record[0]).strftime("%Y-%m-%d %H:%M:%S")
                print(record)
                hist_data.append(record)
            return True
        print('get message as return, retry...')
        time.sleep(0.5)
        return False
    except:
        print('exception here, retry...')
        time.sleep(0.5)
        return False


# log feed failures
def write_log(warning_message):
    log = open('log.txt', 'w')
    for item in warning_message:
        log.write("%s\n" % item)


def get_hist_price(ticker, start_date, periods):
    warning_message = []
    date_range = pd.date_range(start_date, periods=periods, freq='1D')
    for date in date_range:
        print('getting data from {} ...'.format(date))
        hist_eth = []
        time_range = pd.date_range(date, periods=481, freq='3min')
        for i in range(len(time_range) - 1):
            j = 0
            print("getting {} data from {} to {}...".format(ticker, time_range[i], time_range[i + 1]))
            while True:
                if j > 10:
                    print('fail to get data from {} to {}'.format(time_range[i], time_range[i + 1]))
                    warning_message.append("fail to get {} data from {} to {}".format(ticker, time_range[i], time_range[i + 1]))
                    break
                if try_get_feed(ticker.upper()+'-USD', time_range[i], time_range[i+1], hist_eth):
                    if j > 0:
                        print('retry succeeded!')
                    break
                j += 1
        df = pd.DataFrame(hist_eth)
        df.to_csv('data/{}/'.format(ticker.lower()) + date.strftime("%Y-%m-%d") + '.csv', index=False, header=False)
        write_log(warning_message)


def get_start_date_and_time(path, start_date):
    date_range = pd.date_range(start_date, periods=1000, freq='1D')
    for date in date_range:
        if date > datetime.now()+timedelta(days=-1):
            break
        for root, dirs, files in os.walk(path):
            if date.strftime("%Y-%m-%d") + '.csv' in files:
                continue
            else:
                pacific = pytz.timezone('US/Eastern')
                aware = pacific.localize(date, is_dst=None)
                if is_summer_time(aware):
                    date += timedelta(hours=4)
                else:
                    date += timedelta(hours=5)  # if not summer time, 00:00:00 in exchange maps to 05:00:00 locally
                return date


def continue_retrieval(ticker, start_date):
    path = 'data/{}/'.format(ticker)
    start_time = get_start_date_and_time(path, start_date)
    if start_time:
        get_hist_price(ticker, start_time, 200)


ticker = input('This is a data loader application. Type in btc or eth or ltc to get data\n')
start_date = input('since when? you can type a date, for example, 5/1/2017\n')

continue_retrieval(ticker, start_date)
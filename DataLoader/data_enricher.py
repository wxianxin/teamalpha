from datetime import datetime, timedelta
import pandas as pd
import FeatureGenerator.csv_merger as cm
import DataLoader.data_loader as dl
import gdax

# initiate public client
public_client = gdax.PublicClient()
'''
def enrich_all_in_folder(ticker):
    dates = cm.get_dates('1/1/2016', datetime.today().strftime("%Y/%m/%d"), ticker)
    for date in dates:
        enrich_daily_data(date, ticker)


# todo not finished yet
def enrich_daily_data(date, ticker):
    path = 'data/{}/{}.csv'.format(ticker, date)
    df = pd.read_csv(path,header=['time', 'open', 'high', 'low', 'close', 'volumn'])
    drop_list = []
    previous_time = datetime.strptime(date)
    date_time = datetime.strptime(date)
    for index, row in df.iterrows():
        time = datetime.strptime(row['time'])
        if time < date or time > date + timedelta(days = 1):
            drop_list.append(index)
        if index == len(df['time'])-1 and time + timedelta(minutes=3) < date+timedelta(days=1):
            
        if timedelta(minutes=3) < time - previous_time:
            list = []


#todo not finished yet
def get_time_delta(date, ticker, list):
    time_range = pd.date_range(date, periods=5, freq='10min')
    for i in range(5):
        dl.try_get_feed(ticker,time_range[i],time_range[i+1],list, 360)

'''
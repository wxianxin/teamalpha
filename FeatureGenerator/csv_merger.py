from datetime import datetime
import pandas as pd
import os

path = '../DataLoader/data/'

def get_dates(start_date ='7/1/2017', end_date = datetime.today().strftime("%Y/%m/%d"), ticker ='eth'):
    date_range = pd.date_range(start_date,end_date, freq='1D')
    dates = []
    for date in date_range:
        if date > datetime.now():
            break
        for root, dirs, files in os.walk(dir):
            file_name = date.strftime("%Y-%m-%d") + '.csv'
            if file_name in files:
                dates.append(date)
                break
    return dates


def merge_csv(start_date='10/1/2017', end_date='10/9/2017', ticker='eth'):
    dir = path+ticker+'/'
    dates= get_dates(start_date, end_date, ticker)
    with open("raw_data/merged_"+ticker+".csv","wb") as fout:
        for date in dates:
            with open(dir + date.strftime("%Y-%m-%d") + '.csv', "rb") as f:
                fout.write(f.read())


merge_csv('9/1/2017','10/8/2017','eth')
start_date = input('enter start date, for example, 5/1/2017\n')
end_date = input('enter end date, for example, 10/1/2017\n')
ticker = input('enter ticker, for example, eth\n')

print('merging csv files into merged_{}.csv in folder raw_data'.format(ticker))
merge_csv(start_date, end_date, ticker)
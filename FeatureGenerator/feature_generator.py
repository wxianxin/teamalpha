import pandas as pd
import numpy as np


df = pd.read_csv('raw_data/merged_eth.csv', header=None)
df.columns = ['time', 'open', 'high', 'low', 'close', 'vol']
df['time'] = pd.to_datetime(df['time'])
df = df.set_index(['time'])
df['hour'] = df.index.hour
df['minute'] = df.index.minute
df['delta_t'] = 0
df['delta_p'] = 0
df['hist_p_1min'] = 0
df['hist_p_5min'] = 0
df['hist_p_15min'] = 0
df['hist_p_30min'] = 0
df['hist_p_4h'] = 0


prev_p = df.iloc[0, 3]
prev_t = df.index.values[0]
d_ix = df.index

def get_t(datetime_index, time, min_to_subtract):
    time = datetime_index.asof(time-pd.Timedelta(minutes=min_to_subtract))
    try:
        if np.isnan(time):
            return df.index.values[0]
    except:
        return time

for i, row in enumerate(df.values):
    time = df.index.values[i]
    dt = (time - prev_t) / np.timedelta64(1, 's')
    if i == 0:
        continue
    # open, high, low, close, vol, hour, minute, delta_t, delta_p, \
    # hist_p_1min, hist_p_5min, hist_p_15min, hist_p_30min, hist_p_4h = row
    df.set_value(time, 'delta_t', dt)
    df.set_value(time, 'delta_p', row[3] - prev_p)
    df.set_value(time, 'hist_p_1min', df.get_value(get_t(d_ix, time, 1), 'close'))
    df.set_value(time, 'hist_p_5min', df.get_value(get_t(d_ix, time, 5), 'close'))
    df.set_value(time, 'hist_p_15min', df.get_value(get_t(d_ix, time, 15), 'close'))
    df.set_value(time, 'hist_p_30min', df.get_value(get_t(d_ix, time, 30), 'close'))
    df.set_value(time, 'hist_p_4h', df.get_value(get_t(d_ix, time, 240), 'close'))
    prev_t = time
    prev_p = row[3]


df.to_csv('out.csv')
print(df.head())
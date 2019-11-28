import numpy as np
import pandas as pd
from pandas import DataFrame
import gzip
import urllib.request
from datetime import datetime,timedelta
import matplotlib as mpl
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import os

class output_graph():
    def graph(self,yesterday):
        file_date = str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]
        url = f"https://s3-eu-west-1.amazonaws.com/public.bitmex.com/data/trade/{file_date}.csv.gz"
        urllib.request.urlretrieve(url,f"./csv_files/bitmex_csv/trade_{file_date}_fromMEX.csv.gz")
        bitmex = []
        index = []
        with gzip.open(f"./csv_files/bitmex_csv/trade_{file_date}_fromMEX.csv.gz","r") as f:
            for row in f:
                string_row = str(row)[2:len(row)+1].split(",")
                if string_row[1] == "XBTUSD" or string_row[0] == "timestamp":
                    bitmex.append(string_row[1:])
                    if string_row[0] != "timestamp":
                        index.append(datetime.strptime(string_row[0][:10]+" " + string_row[0][11:19],'%Y-%m-%d %H:%M:%S') + timedelta(hours = 9))
        df_mex = pd.DataFrame(bitmex[1:],columns = bitmex[0],index = index)
        df_mex = df_mex.drop("symbol",axis = 1)
        df_mex =df_mex.drop("side",axis = 1)
        df_mex =df_mex.drop("tickDirection",axis = 1)
        df_mex =df_mex.drop("trdMatchID",axis = 1)
        df_mex =df_mex.drop("grossValue",axis = 1)
        df_mex =df_mex.drop("homeNotional",axis = 1)
        df_mex =df_mex.drop("foreignNotional",axis = 1)
        df_mex = df_mex.astype(float)
        date = str(yesterday)[:4]+"-"+str(yesterday)[5:7]+"-"+str(yesterday)[8:10]
        one_day_after = yesterday + timedelta(days = 1)
        date_2 = str(one_day_after)[:4]+"-"+str(one_day_after)[5:7]+"-"+str(one_day_after)[8:10]

        file_date = date[0:4]+date[5:7]+date[8:10]

        parser = lambda date: pd.to_datetime(date, format='%Y-%m-%dD%H:%M:%S.%f000')
        api_header = ['timestamp', 'price', 'size']
        df_bf = pd.read_csv(f'./csv_files/bitflyer_BTCJPY_{file_date}.csv', names=api_header, index_col=0, parse_dates=True)#, date_parser=parser)#[0])
        bf_ohlc = df_bf['price'].resample('S').ohlc().fillna(method='ffill')
        df_lq = pd.read_csv(filepath_or_buffer=f'./csv_files/liquid_BTCJPY_{file_date}.csv', names=api_header, index_col=0, parse_dates=True)#, date_parser=parser)#[0])
        lq_ohlc = df_lq['price'].resample('S').ohlc().fillna(method='ffill')
        mex_ohlc = df_mex['price'].resample('S').ohlc().fillna(method='ffill')
        mexbf = pd.merge(bf_ohlc["open"], mex_ohlc["open"], how="right", left_index=True, right_index=True, suffixes=['_bf', '_mex'])
        tri = pd.merge(mexbf, lq_ohlc["open"], how="left", left_index=True, right_index=True)
        for i in range(24):
            if i < 14:
                tri_prox = tri[tri.index > f"{date} {9+i}:00:00"]
                tri_prox = tri_prox[tri_prox.index < f"{date} {10+i}:00:00"]
            elif i == 14:
                tri_prox = tri[tri.index > f"{date} 23:00:00"]
                tri_prox = tri_prox[tri_prox.index < f"{date_2} 00:00:00"]
            else:
                tri_prox = tri[tri.index > f"{date_2} {i-15}:00:00"]
                tri_prox = tri_prox[tri_prox.index < f"{date_2} {i-14}:00:00"]
            fig, ax1 = plt.subplots(figsize=(18,9))
            ax2 = ax1.twinx()

            ax1.plot(tri_prox["open_bf"],color = "red",label = "bitflyer")
            ax1.plot(tri_prox["open"],color="black", label = "liquid")
            ax2.plot(tri_prox["open_mex"], label = "bitmex")
            ax1.legend()
            ax2.legend(loc = 3)
            os.makedirs(f"./graphs/{file_date}", exist_ok=True)
            plt.savefig(f'./graphs/{file_date}/all_graph_{date}_{i+1}.png')
            plt.close()
        # plt.savefig(f'./trading graph/20191109-1111/all_graph_{date}_{i+1}.png')

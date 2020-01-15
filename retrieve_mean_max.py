import csv 
from datetime import datetime, timezone, timedelta
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import os
import gzip
import urllib.request
import numpy as np
import math
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter



class price_diff():
    def run(self,yesterday):
        file_date = str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]
        bitmex = []
        liquid = []

        url = f"https://s3-eu-west-1.amazonaws.com/public.bitmex.com/data/trade/{file_date}.csv.gz"
        urllib.request.urlretrieve(url,f"C:/Users/mrspo/Documents/intern/trading data/codes/get_trading_data/csv_files/bitmex_csv/{file_date}.csv.gz")
        
        with gzip.open(f"./csv_files/bitmex_csv/{file_date}.csv.gz","r") as f:
            for row in f:
                string_row = str(row)[2:len(row)+1].split(",")
                if string_row[1] == "XBTUSD" and string_row[0] != "timestamp":
                    bitmex.append(string_row)
        
        with open(f"./csv_files/liquid_BTCJPY_{file_date}.csv","r") as f:
            reader = csv.reader(f, lineterminator = "\n")
            for row in reader:
                liquid.append(row)

        def close_price_find(execution,correct_time):
            count = 0
            return_exec = 0
            for one_exec in execution:
                this_time = one_exec[0][:19]
                this_datetime = datetime.strptime(this_time,'%Y-%m-%d %H:%M:%S')
                if this_datetime < correct_time:
                    return_exec = one_exec[1]
                    count += 1
                else:
                    break 
            if return_exec != 0:
                del execution[0:count-1] 
            return return_exec,execution

        def close_price_find_bitmex(execution,correct_time):
            count = 0
            return_exec = 0
            for one_exec in execution:
                this_time = one_exec[0][:10]+" " + one_exec[0][11:19]
                this_datetime = datetime.strptime(this_time,'%Y-%m-%d %H:%M:%S') + timedelta(hours = 9)
                if this_datetime <= correct_time:
                    return_exec = one_exec[4]
                    count += 1
                else:
                    break 
            if return_exec != 0:
                del execution[0:count-1] 
            return return_exec,execution
        
        flag = True
        rate = 108.080000
        now_string = liquid[0][0][:10]+ " " + liquid[0][0][11:19]
        now = datetime.strptime(now_string,'%Y-%m-%d %H:%M:%S')
        price_diff = []
        end_time = yesterday + timedelta(days = 1)
        date = []
        while flag:
            bitmex_one_exec,bitmex = close_price_find_bitmex(bitmex,now)
            liquid_one_exec,liquid = close_price_find(liquid,now)
            bitmex_one_exec = float(bitmex_one_exec)
            liquid_one_exec = float(liquid_one_exec)
            if math.floor(bitmex_one_exec) != 0 and math.floor(liquid_one_exec) != 0:
                price_diff.append(abs(bitmex_one_exec*rate-liquid_one_exec))
                date.append(now)
            if end_time < now:
                flag = False
            now = now + timedelta(seconds=1)
        price_diff_array = np.array(price_diff)
        average_price_diff = np.average(price_diff_array)
        max_bitmex = np.amax(price_diff_array)

        print(yesterday,average_price_diff,max_bitmex)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.plot(date,price_diff)
        plt.title(f"price difference: {yesterday.year}-{yesterday.month}-{yesterday.day}")
        plt.xlabel("time")
        plt.ylabel("price diff (absolute value)")
        # plt.xticks(np.arange(min(date), max(date), 6*60*60))
        ax.xaxis.set_major_locator(plt.MaxNLocator(4))
        ax.xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))
        plt.show()

        

if __name__ == "__main__":
    now = datetime.now() 
    now = now.replace(hour=9,minute=0,second=0,microsecond=0)
    now = now -timedelta(days = 4)
    yesterday = now-timedelta(days = 1)
    parser = price_diff()
    parser.run(yesterday)
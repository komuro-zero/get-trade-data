from __future__ import unicode_literals, print_function

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pybitflyer
import time
import pytz 
from quoine.client import Quoinex
from datetime import datetime, timedelta
import bitmex
import csv
from pytz import timezone
import os

class bitmex_BTCUSD():
    def to_japan_time(self,input_time):
        new_time = input_time + timedelta(hours = 9)
        txt = new_time.strftime("%Y-%m-%d %H:%M:%S")
        output_time = datetime.strptime(txt,"%Y-%m-%d %H:%M:%S")
        return output_time


    def run(self,now,yesterday):
        count = 1000
        bitmex_api = bitmex.bitmex()
        start_time = yesterday.astimezone(timezone('UTC'))
        now_bmx = now.astimezone(timezone("UTC"))
        bitmex_executions =  bitmex_api.Trade.Trade_get(symbol="XBTUSD",startTime = start_time, count= 1).result()
        first_price = bitmex_executions[0][0]["price"]
        first_timestamp = bitmex_executions[0][0]["timestamp"]
        last_execution_timestamp = first_timestamp 


        #run algorithm
        flag = True
        all_price = [first_price]
        all_time = [self.to_japan_time(first_timestamp)]
        csv_data = []
        count = 0
        while flag:
            bitmex_execution = bitmex_api.Trade.Trade_get(symbol="XBTUSD", startTime= start_time,count=1000).result()
            last_time = bitmex_execution[0][0]["timestamp"]
            last_price = bitmex_execution[0][0]["price"]
            if now_bmx > last_time:
                for execution in bitmex_execution[0]:
                    now_time = execution['timestamp']
                    now_price = execution["price"]
                    all_price.append(now_price)
                    all_time.append(self.to_japan_time(now_time))

            else:
                flag = False
            for i in range(len(all_price)):
                csv_data.append([all_time[i],all_price[i]])
            time.sleep(2)
            count += 1
            start_time = bitmex_execution[0][-1]["timestamp"]
            os.makedirs("./csv_files/", exist_ok=True)
            with open(f"./csv_files/bitmex_BTCUSD_{str(now)[:4]+str(now)[5:7]+str(now)[8:10]}.csv","a") as f:
                writer = csv.writer(f,lineterminator = "\n")
                writer.writerows(csv_data)
            csv_data= []
            all_price = []
            all_time = []
            this_execution_timestamp = bitmex_execution[0][0]["timestamp"]
            if this_execution_timestamp == last_execution_timestamp:
                start_time = start_time + timedelta(seconds = 1)
            last_execution_timestamp = this_execution_timestamp 

if __name__ == "__main__":
    now = datetime.now(timezone("Asia/Tokyo"))
    now = now.replace(microsecond=0)
    yesterday = now-timedelta(days = 1)
    run = bitmex_BTCJPY()
    run.run(now,yesterday)    
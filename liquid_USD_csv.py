from __future__ import unicode_literals, print_function

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import pytz 
from quoine.client import Quoinex
from datetime import datetime, timezone, timedelta
import csv
from time import sleep
import os

class liquid_BTCUSD():
        
    def liquid_quantify_executions(self,liquid_executions):
        liquid_price = []
        liquid_time = []
        last_time = datetime.fromtimestamp(liquid_executions[0]["created_at"]).strftime('%Y-%m-%d %H:%M:%S')
        for liquid_execution in liquid_executions:
            this_time = datetime.fromtimestamp(liquid_execution["created_at"])
            if this_time != last_time:
                liquid_price.append(liquid_execution["price"])
                liquid_time.append(this_time.strftime('%Y-%m-%d %H:%M:%S'))
                last_time = this_time
        return liquid_price, liquid_time

    def run(self,now,yesterday,liquid_sleep_time,lqd_USD_time = None):
        product_id = 1
        limit = 1000
        quoine = Quoinex("","")
        if lqd_USD_time:
            timestamp = lqd_USD_time.timestamp()
        else:
            timestamp = yesterday.timestamp()
        now_lqd = now.timestamp()
        flag = True

        while flag:
            all_csv = []
            liquid_executions = quoine.get_executions_since_time(product_id= product_id ,timestamp = timestamp,limit = limit)
            price, time = self.liquid_quantify_executions(liquid_executions)
            for i in range(len(price)):
                all_csv.append([time[i],price[i]])
            timestamp = liquid_executions[-1]["created_at"]
            os.makedirs("./csv_files/", exist_ok=True)            
            with open(f"./csv_files/liquid_BTCUSD_{str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]}.csv","a") as f:
                writer = csv.writer(f, lineterminator = "\n")
                writer.writerows(all_csv)
            print(f"liquid USD, date: {time[0]}")
            if now_lqd < timestamp:
                flag = False
            sleep(liquid_sleep_time)
from __future__ import unicode_literals, print_function

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pybitflyer
import time
import pytz 
from quoine.client import Quoinex
from datetime import datetime, timezone, timedelta
import bitmex
import csv
from time import sleep

class liquid_BTCJPY():
        
    def liquid_quantify_executions(liquid_executions):
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
    def run(now,yesterday):
        product_id = 5
        limit = 1000
        quoine = Quoinex("","")
        flag = True
        count = 0
        timestamp = yesterday

        while flag:
            all_csv = []
            all_time = []
            liquid_executions = quoine.get_executions_since_time(product_id= product_id ,timestamp = timestamp,limit = limit)
            price, time = liquid_quantify_executions(liquid_executions)
            now = liquid_executions[0]["created_at"]
            print(" ",datetime.fromtimestamp(liquid_executions[0]["created_at"]),"\n",datetime.fromtimestamp(liquid_executions[-1]["created_at"]),"\n","======================================")
            for i in range(len(price)):
                all_csv.append([time[i],price[i]])
            timestamp = liquid_executions[-1]["created_at"]
            count += 1
            with open("./liquid_BTCUSD.csv","a") as f:
                writer = csv.writer(f, lineterminator = "\n")
                writer.writerows(all_csv)
            if end_date < timestamp:
                flag = False
            sleep(2)
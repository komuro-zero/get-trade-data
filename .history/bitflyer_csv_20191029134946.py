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

class bitflyer():
    
    #yesterday = datetime.today() - timedelta(days=1)
    def convert_time(time):
        new_time = time[:10]+ " " + time[11:]
        altered_time = datetime.strptime(new_time[:19],'%Y-%m-%d %H:%M:%S') + timedelta(hours = 9)
        return altered_time

    def bitflyer_quantify_executions(executions):
        price = []
        date = []
        for execution in executions:
            this_time = convert_time(execution["exec_date"])
            price.append(execution["price"])
            date.append(this_time)
        return price, date
    #bitflyer
    def run(self,now,yesterday):
        bitflyer_api = pybitflyer.API()
        product_code = "BTC_JPY"

        #first get the execution id for the most recent transaction made
        price = []
        all_price = []
        date = []
        all_date = []
        count =0
        #based on the timestamp, get the transaction for last 500 transactions. continue to do so with the last transaction id for each iteration until you reach the next day.

        flag = True
        while flag:
            if count == 0:
                executions = bitflyer_api.executions(product_code = product_code, count = 500)
                one_week_ago = convert_time(executions[0]["exec_date"])- timedelta(days = 60)
            else:
                executions = bitflyer_api.executions(product_code = product_code,before = before_id, count = 500)
            print(executions)
            before_id = executions[-1]["id"]
            price, date = bitflyer_quantify_executions(executions)
            csv_data = []
            for i in range(len(price)):
                csv_data.append([date[i],price[i]])
            last_day = date[0]
            print(price[0])
            if one_week_ago > last_day:
                flag = False
            else:
                with open(f"bitflyer_BTCJPY_{}.csv","a") as f:
                    writer = csv.writer(f,lineterminator='\n')
                    for data in csv_data:
                        writer.writerow(data)
                    
            time.sleep(1)
            count +=1


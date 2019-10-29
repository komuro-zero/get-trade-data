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

class bitflyer_BTCJPY():
    def convert_time(self,time):
        new_time = time[:10]+ " " + time[11:]
        altered_time = datetime.strptime(new_time[:19],'%Y-%m-%d %H:%M:%S') + timedelta(hours = 9)
        return altered_time

    def bitflyer_quantify_executions(self,executions):
        price = []
        date = []
        for execution in executions:
            this_time = self.convert_time(execution["exec_date"])
            price.append(execution["price"])
            date.append(this_time)
        return price, date

    def run(self,now,yesterday):
        bitflyer_api = pybitflyer.API()
        product_code = "BTC_JPY"

        #first get the execution id for the most recent transaction made
        price = []
        date = []
        count =0
        #based on the timestamp, get the transaction for last 500 transactions. continue to do so with the last transaction id for each iteration until you reach the next day.

        flag = True
        while flag:
            if count == 0:
                executions = bitflyer_api.executions(product_code = product_code, count = 1001)
            else:
                executions = bitflyer_api.executions(product_code = product_code,before = before_id, count = 500)
            before_id = executions[-1]["id"]
            price, date = self.bitflyer_quantify_executions(executions)
            csv_data = []
            print(executions)
            for i in range(len(price)):
                csv_data.append([date[i],price[i]])
            last_day = date[0]
            if yesterday > last_day:
                flag = False
            else:
                with open(f"./csv_files/bitflyer_BTCJPY_{str(now)[:4]+str(now)[5:7]+str(now)[8:10]}.csv","a") as f:
                    writer = csv.writer(f,lineterminator='\n')
                    for data in csv_data:
                        writer.writerow(data)
                    
            time.sleep(1)
            count +=1

if __name__ == "__main__":
    run = bitflyer_BTCJPY()
    now = datetime.now()
    yesterday = now -timedelta(days = 1)
    run.run(now,yesterday)
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
import os


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

    def run(self,now,yesterday,bitflyer_sleep_time,product_codes,before_id = None):
        bitflyer_api = pybitflyer.API()
        yesterday = yesterday.replace(tzinfo=None)
        now = now.replace(tzinfo=None)

        #first get the execution id for the most recent transaction made
        price = []
        date = []
        count =0
        #based on the timestamp, get the transaction for last 500 transactions. continue to do so with the last transaction id for each iteration until you reach the next day.

        flag = True
        while flag:
            if not before_id:
                executions = bitflyer_api.executions(product_code = product_codes, count = 500)
            else:
                executions = bitflyer_api.executions(product_code = product_codes,before = before_id, count = 500)
            before_id = executions[-1]["id"]
            price, date = self.bitflyer_quantify_executions(executions)
            if date[0] < now:
                csv_data = []
                for i in range(len(price)):
                    csv_data.append([date[i],price[i]])
                last_day = date[0]
                if yesterday > last_day:
                    flag = False
                else:
                    os.makedirs("./csv_files/", exist_ok=True)
                    with open(f"./csv_files/bitflyer_{product_codes}_{str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]}.csv","a") as f:
                        writer = csv.writer(f,lineterminator='\n')
                        for data in csv_data:
                            writer.writerow(data)
                    print(f"bitflyer, date: {date[0]} id: {before_id}")
            time.sleep(bitflyer_sleep_time)
            print(date[0],now)
            count +=1
    
    def test_run(self,now,yesterday):
        product_codes = "FX_BTC_JPY"
        bitflyer_api = pybitflyer.API()
        yesterday = yesterday.replace(tzinfo=None)
        now = now.replace(tzinfo=None)
        before_id= None

        #first get the execution id for the most recent transaction made
        price = []
        date = []
        count =0
        #based on the timestamp, get the transaction for last 500 transactions. continue to do so with the last transaction id for each iteration until you reach the next day.

        flag = True
        while flag:
            if not before_id:
                executions = bitflyer_api.executions(product_code = product_codes, count = 3)
            else:
                print(before_id)
                executions = bitflyer_api.executions(product_code = product_codes,after = before_id, count = 3)
            before_id = executions[0]["id"]
            time.sleep(2)
            for row in executions:
                print(before_id,row)
            count +=1

if __name__ == "__main__":
    bitflyer = bitflyer_BTCJPY()
    now = datetime.now()
    yesterday = now -timedelta(days = 1)
    bitflyer.test_run(now,yesterday)
from binance.client import Client
from datetime import datetime, timedelta
import os
import csv
import time


class binance_BTCUSD():
    def __init__(self):
            
        self.api_key = "aA5xb2MhRUVfPgR4DIIMipezMbPrUfwO9vNgRkPsozSRgw6YSoRL7BT5lCtH2eYE"
        self.api_secret = "zwENZoYrE2LnEbjL06EOxsnXgzIAB8UtU6z8ysK2WbjpiFETPMF7Hi7jViz56SWK"
        self.currency_symbol = "BTCUSDT"
        self.transaction_limit = 1000
        self.until_str = (datetime.now())
        self.from_str = (datetime.now() - timedelta(hours = 1))

    def to_japan_datetime(self,timestamp):
        utc_datetime = datetime.fromtimestamp(timestamp/1000)
        japan_datetime = utc_datetime #+ timedelta(hours = 9)
        return japan_datetime

    def get_binance_transaction(self,end_time,start_time):
        end_time = end_time.replace(tzinfo=None)
        start_time = start_time.replace(tzinfo=None)
        continue_flag = True
        binance_client = Client(api_key=self.api_key, api_secret=self.api_secret)
        # oldest_point=
        # newest_point=
        historical_data = binance_client.get_historical_trades(symbol=self.currency_symbol,limit = self.transaction_limit)
        last_id = historical_data[-1]["id"]
        all_csv = []
        count = 0
        
        while continue_flag:
            historical_data = binance_client.get_historical_trades(symbol=self.currency_symbol,limit = self.transaction_limit,fromId = last_id)
            last_id = historical_data[0]["id"]-1000
            last_time = self.to_japan_datetime(historical_data[-1]["time"])

            if last_time < end_time:
                for row in historical_data:
                    all_csv.insert(0,[self.to_japan_datetime(row["time"]),row["price"]])
                os.makedirs("./csv_files/", exist_ok=True)
                with open(f"./csv_files/binance_BTCUSDT_{str(start_time)[:4]+str(start_time)[5:7]+str(start_time)[8:10]}.csv","a") as f:
                    writer = csv.writer(f, lineterminator = "\n")
                    writer.writerows(all_csv)
                all_csv = []
            if last_time < start_time:
                continue_flag = False
            time.sleep(2)
            print(f"count:{count}",(historical_data[0]["id"]),(historical_data[-1]["id"])) 
            count += 1

if __name__ == "__main__":
    binance = binance()
    binance.get_binance_transaction()

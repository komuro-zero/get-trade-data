from bitflyer_csv import bitflyer_BTCJPY
from bitmex_csv import bitmex_BTCUSD
from liquid_csv import liquid_BTCJPY
from liquid_USD_csv import liquid_BTCUSD
from binance_csv import binance_BTCUSD
from csv_to_graph_JPY import JPY_csv_to_graph
from csv_to_graph_USD import USD_csv_to_graph
from parse import parse
from datetime import datetime,timedelta
from pytz import timezone
from upload import upload
import traceback


class job():
    def run(self,days_before,bf_id,lqd_JPY_time,lqd_USD_time,get_bf,get_lqd_JPY,get_lqd_USD,bitflyer_sleep_time,liquid_sleep_time):
        now = datetime.now(timezone("Asia/Tokyo")) #-timedelta(days = 1)
        now = now.replace(hour=9,minute=0,second=0,microsecond=0)
        yesterday = now-timedelta(days = 1)
        start_date = now-timedelta(days = days_before)

        if get_bf:
            btf = bitflyer_BTCJPY()
            btf.run(now,start_date,bitflyer_sleep_time,"BTC_JPY",bf_id)
            btf.run(now,start_date,bitflyer_sleep_time,"FX_BTC_JPY",bf_id)
        if get_lqd_JPY:
            lqdjpy = liquid_BTCJPY()
            lqdjpy.run(now,start_date,liquid_sleep_time,lqd_JPY_time)
        if get_lqd_USD:
            lqdusd = liquid_BTCUSD()
            lqdusd.run(now,start_date,liquid_sleep_time,lqd_USD_time)
        get_binance_USD = binance_BTCUSD()
        get_binance_USD.get_binance_transaction(now,start_date)
        graph_jpy = JPY_csv_to_graph()
        graph_jpy.run(yesterday)
        graph_usd = USD_csv_to_graph()
        graph_usd.run(yesterday)
        drive_upload = upload()
        drive_upload.upload_photo(yesterday)



if __name__ == "__main__":
    #さかのぼる日数。
    days_before = 1

    #情報をとってくるかどうか
    get_bf = True
    get_lqd_JPY = True
    get_lqd_USD = True

    # 途中から実行したい場合
    bf_id = None
    lqd_JPY_time = None
    # lqd_JPY_time = datetime.strptime('2019-00-00 00:00:00','%Y-%m-%d %H:%M:%S')
    lqd_USD_time = None
    # lqd_USD_time = datetime.strptime('2019-00-00 00:00:00','%Y-%m-%d %H:%M:%S')
    bitflyer_sleep_time = 2
    liquid_sleep_time = 1.5

    try:
        job = job()
        job.run(days_before,bf_id,lqd_JPY_time,lqd_USD_time,get_bf,get_lqd_JPY,get_lqd_USD,bitflyer_sleep_time,liquid_sleep_time)
    except:
        traceback.print_exc()

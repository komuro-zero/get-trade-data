from bitflyer_csv import bitflyer_BTCJPY
from bitmex_csv import bitmex_BTCUSD
from liquid_csv import liquid_BTCJPY
from liquid_USD_csv import liquid_BTCUSD
from csv_to_graph import output_graph
from parse import parse
from datetime import datetime,timedelta
from pytz import timezone
from upload import upload
import traceback


class job():
    def run(self,days_before,bf_id,lqd_JPY_time,lqd_USD_time,get_bf,get_lqd_JPY,get_lqd_USD,bitflyer_sleep_time,liquid_sleep_time):
        now = datetime.now(timezone("Asia/Tokyo")) -timedelta(days = 1)
        now = now.replace(hour=9,minute=0,second=0,microsecond=0)
        yesterday = now-timedelta(days = 1)
        start_date = now-timedelta(days = days_before)

        if get_bf:
            btf = bitflyer_BTCJPY()
            btf.run(now,start_date,bf_id,bitflyer_sleep_time)
        if get_lqd_JPY:
            lqdjpy = liquid_BTCJPY()
            lqdjpy.run(now,start_date,lqd_JPY_time,liquid_sleep_time)
        if get_lqd_USD:
            lqdusd = liquid_BTCUSD()
            lqdusd.run(now,start_date,lqd_USD_time,liquid_sleep_time)
        graph = output_graph()
        graph.graph(yesterday)
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
    bitflyer_sleep_time = 1
    liquid_sleep_time = 2

    job = job()
    try:
        job.run(days_before,bf_id,lqd_JPY_time,lqd_USD_time,get_bf,get_lqd_JPY,get_lqd_USD,bitflyer_sleep_time,liquid_sleep_time)
    except:
        traceback.print_exc()

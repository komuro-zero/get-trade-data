from bitflyer_csv import bitflyer_BTCJPY
from bitmex_csv import bitmex_BTCUSD
from liquid_csv import liquid_BTCJPY
from liquid_USD_csv import liquid_BTCUSD
from parse import parse
from datetime import datetime,timedelta
from pytz import timezone

class job():
    def run(self,days_before):
        now = datetime.now(timezone("Asia/Tokyo"))
        now = now.replace(microsecond=0)
        start_date = now-timedelta(days = days_before)

        btf = bitflyer_BTCJPY()
        btf.run(now,start_date)
        bmx = bitmex_BTCUSD()
        bmx.run(now,start_date)
        lqdjpy = liquid_BTCJPY()
        lqdjpy.run(now,start_date)
        lqdusd = liquid_BTCUSD()
        lqdusd.run(now,start_date)
        parser = parse()
        parser.run(days_before)


if __name__ == "__main__":
    days_before = 1
    run = job()
    run.run(days_before)
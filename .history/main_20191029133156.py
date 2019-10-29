from bitflyer_csv import bitflyer_BTCJPY
from bitmex_csv import bitmex_BTCUSD
from liquid_csv import liquid_BTCJPY
from liquid_USD_csv import liquid_BTCUSD
from parse import parse
from datetime import datetime,timedelta
from pytz import timezone


if __name__ == "__main__":
    now = datetime.now(timezone("Asia/Tokyo"))
    now = now.replace(microsecond=0)
    yesterday = now-timedelta(days = 1)

    # btf = bitflyer_BTCJPY()
    # btf.run(now,yesterday)
    # bmx = bitmex_BTCUSD()
    # bmx.run(now,yesterday)
    # lqdjpy = liquid_BTCJPY()
    # lqdjpy.run(now,yesterday)
    # lqdusd = liquid_BTCUSD()
    # lqdusd.run(now,yesterday)
    parse = parse()
    parse.run()
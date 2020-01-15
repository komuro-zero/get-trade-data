import csv 
from datetime import datetime, timezone, timedelta
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import os
import gzip
import urllib.request


class USD_csv_to_graph():
    def run(self,yesterday):
        file_date = str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]
        binance = []
        bitmex = []
        liquid = []

        with open(f"./csv_files/binance_BTCUSDT_{file_date}.csv","r") as f:
            reader = csv.reader(f, lineterminator = "\n")
            for row in reader:
                binance.append(row)
        binance.reverse()

        url = f"https://s3-eu-west-1.amazonaws.com/public.bitmex.com/data/trade/{file_date}.csv.gz"
        urllib.request.urlretrieve(url,f"C:/Users/mrspo/Documents/intern/trading data/codes/get_trading_data/csv_files/bitmex_csv/{file_date}.csv.gz")
        with gzip.open(f"./csv_files/bitmex_csv/{file_date}.csv.gz","r") as f:
            for row in f:
                string_row = str(row)[2:len(row)+1].split(",")
                if string_row[1] == "XBTUSD" and string_row[0] != "timestamp":
                    bitmex.append(string_row)
        
        with open(f"./csv_files/liquid_BTCUSD_{file_date}.csv","r") as f:
            reader = csv.reader(f, lineterminator = "\n")
            for row in reader:
                liquid.append(row)

        def close_price_find(execution,correct_time):
            count = 0
            return_exec = None
            for one_exec in execution:
                this_time = one_exec[0][:19]
                this_datetime = datetime.strptime(this_time,'%Y-%m-%d %H:%M:%S')
                if this_datetime < correct_time:
                    return_exec = one_exec[1]
                    count += 1
                else:
                    break 
            if return_exec != None:
                del execution[0:count-1] 
            return return_exec,execution

        def close_price_find_bitmex(execution,correct_time):
            count = 0
            for one_exec in execution:
                this_time = one_exec[0][:10]+" " + one_exec[0][11:19]
                this_datetime = datetime.strptime(this_time,'%Y-%m-%d %H:%M:%S') + timedelta(hours = 9)
                if this_datetime <= correct_time:
                    return_exec = one_exec[4]
                    count += 1
                else:
                    break 
            del execution[0:count-1] 
            return return_exec,execution
        

        flag = True
        now_string = bitmex[0][0][:10]+ " " + bitmex[0][0][11:19]
        now = datetime.strptime(now_string,'%Y-%m-%d %H:%M:%S')+ timedelta(hours = 9)
        graph_binance_usd = []
        graph_bmx_usd = []
        graph_lqd_usd = []
        graph_axis_time = []
        graph_time = now + timedelta(hours = 1)
        all_trade_exec =[]
        counter = 0
        graph_counter = 1
        while flag:
            print(now)
            bitmex_one_exec,bitmex = close_price_find_bitmex(bitmex,now)
            liquid_one_exec,liquid = close_price_find(liquid,now)
            binance_one_exec,binance = close_price_find(binance,now)
            bitmex_one_exec = float(bitmex_one_exec)
            all_trade_exec.append([now,bitmex_one_exec,liquid_one_exec,binance_one_exec])
            if counter == 0:
                graph_bmx_usd = [float(bitmex_one_exec)]
                graph_lqd_usd = [float(liquid_one_exec)]
                graph_binance_usd = [float(binance_one_exec)]
                graph_axis_time = [now]
            else:
                graph_bmx_usd.append(float(bitmex_one_exec))
                graph_lqd_usd.append(float(liquid_one_exec))
                graph_binance_usd.append(float(binance_one_exec))
                graph_axis_time.append(now)
            now = now + timedelta(seconds = 1)
            counter += 1
            if counter % 1000 == 0:
                with open(f"./csv_files/all_trade_data_USD_{str(now)[:4]+str(now)[5:7]+str(now)[8:10]}.csv","a") as f:
                    writer = csv.writer(f,lineterminator="\n")
                    writer.writerows(all_trade_exec)
                all_trade_exec = []
            if graph_time < now:

                # plot
                plt.plot(graph_axis_time, graph_bmx_usd, color='b', label='bitmex BTCUSD')
                plt.plot(graph_axis_time, graph_lqd_usd, color='y', label='liquid BTCUSD')
                plt.plot(graph_axis_time, graph_binance_usd, color='g', label='binance BTCUSD')

                # x axis
                #plt.locator_params(axis='x', nbins=5)
                plt.xlabel('time')

                # y axis
                plt.ylabel('price USD')

                # legend and title
                plt.legend(loc='best')
                plt.title(f'BTCUSD {now}')
                os.makedirs("./graphs/", exist_ok=True)


                # save as png
                plt.savefig(f"./graphs/BTCUSD_{str(now)[:4]+str(now)[5:7]+str(now)[8:10]}_{graph_counter}.png")
                graph_bmx_usd = [float(bitmex_one_exec)]
                graph_lqd_usd = [float(liquid_one_exec)]
                graph_binance_usd = [float(binance_one_exec)]
                graph_axis_time = [now]
                graph_time = now + timedelta(hours = 1)
                graph_counter += 1
                plt.close()
            if len(bitmex) < 5:
                flag = False

if __name__ == "__main__":
    now = datetime.now(timezone("Asia/Tokyo"))
    now = now.replace(hour=0,minute=0,second=0,microsecond=0)
    yesterday = now-timedelta(days = 1)
    parser = USD_csv_to_graph()
    # parser.run()
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



class gz_parse():
    def run(self,yesterday):
        file_date = str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]
        bitmex = []
        # url = f"https://s3-eu-west-1.amazonaws.com/public.bitmex.com/data/trade/{file_date}.csv.gz"
        # urllib.request.urlretrieve(url,f"C:/Users/mrspo/Documents/intern/trading data/codes/get_trading_data/csv_files/bitmex_csv/{file_date}.csv.gz")
        with gzip.open(f"./csv_files/bitmex_csv/{file_date}.csv.gz","r") as f:
            for row in f:
                string_row = str(row)[2:len(row)+1].split(",")
                if string_row[1] == "XBTUSD" and string_row[0] != "timestamp":
                    bitmex.append(string_row)
        liquid = []
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
                count += 1
                if this_datetime <= correct_time:
                    return_exec = float(one_exec[1])
                else:
                    break 
            if count > 10:
                del execution[0:count-10] 
            return return_exec,execution

        def close_price_find_bitmex(execution,correct_time):
            count = 0
            return_exec = None
            one_second_volume = 0
            for one_exec in execution:
                this_time = one_exec[0][:10]+" " + one_exec[0][11:19]
                this_datetime = datetime.strptime(this_time,'%Y-%m-%d %H:%M:%S') + timedelta(hours = 9)
                count += 1
                if this_datetime <= correct_time:
                    return_exec = float(one_exec[4])
                    if correct_time-timedelta(seconds=1) < this_datetime:
                        one_second_volume += float(one_exec[3])
                else:
                    break 
            if count > 10:
                del execution[0:count-10] 
            return return_exec,one_second_volume,execution

        flag = True
        now_string = bitmex[0][0][:10]+ " " + bitmex[0][0][11:19]
        now = datetime.strptime(now_string,'%Y-%m-%d %H:%M:%S') + timedelta(hours = 9)
        graph_bmx_usd = []
        graph_lqd_usd = []
        bitmex_volume = []
        graph_axis_time = []
        graph_time = now + timedelta(hours = 1)
        all_trade_exec =[]
        counter = 0
        graph_counter = 1
        while flag:
            bitmex_one_exec,one_bitmex_volume,bitmex = close_price_find_bitmex(bitmex,now)
            liquid_one_exec,liquid = close_price_find(liquid,now)
            all_trade_exec.append([now,bitmex_one_exec,one_bitmex_volume])
            if counter == 0:
                graph_bmx_usd = [bitmex_one_exec]
                graph_lqd_usd = [liquid_one_exec]
                bitmex_volume = [one_bitmex_volume]
                graph_axis_time = [now]
            else:
                graph_bmx_usd.append(bitmex_one_exec)
                graph_lqd_usd.append(liquid_one_exec)
                bitmex_volume.append(one_bitmex_volume)
                graph_axis_time.append(now)
            now = now + timedelta(seconds = 1)
            counter += 1
            if counter % 1000 == 0:
                with open(f"./csv_files/all_trade_data_USD_{file_date}.csv","a") as f:
                    writer = csv.writer(f,lineterminator="\n")
                    writer.writerows(all_trade_exec)
            if graph_time < now:
                fig = plt.figure()
                ax = fig.add_subplot(2, 1, 1)

                # plot
                ax.plot(graph_axis_time, graph_bmx_usd, color='b', label='bitmex BTCUSD')
                ax.plot(graph_axis_time, graph_lqd_usd, color='#e46409', label='liquid BTCUSD')

                # x axis
                #plt.locator_params(axis='x', nbins=5)
                ax.set_xlabel('time')

                # y axis
                ax.set_ylabel('price USD')

                # legend and title
                ax.legend(loc='best')
                ax.set_title(f'bitmex USD {now}')
                os.makedirs("./graphs/", exist_ok=True)
                ax2 = fig.add_subplot(2, 1, 2)
                ax2.plot(graph_axis_time,bitmex_volume,color = "red",label="bitmex trade volume")


                # save as png
                plt.savefig(f"./graphs/bitmexcsv_USD_{file_date}_{graph_counter}.png")
                graph_bmx_usd = [bitmex_one_exec]
                graph_axis_time = [now]
                graph_time = now + timedelta(hours = 1)
                graph_counter += 1
                plt.close()
                all_trade_exec = []
                graph_bmx_usd = [bitmex_one_exec]
                graph_lqd_usd = [liquid_one_exec]
                bitmex_volume = [one_bitmex_volume]
            if len(bitmex) < 15:
                flag = False

if __name__ == "__main__":
    now = datetime.now(timezone("Asia/Tokyo"))
    now = now.replace(hour=0,minute=0,second=0,microsecond=0)
    yesterday = now-timedelta(days = 1)
    parser = parse()
    parser.run()
import csv 
from datetime import datetime, timezone, timedelta
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import os


class csv_parse():
    def run(self,yesterday):
        file_date = str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]
        bitmex = []
        with open(f"./csv_files/bitmex_csv/trade_{file_date}.csv","r") as f:
            reader = csv.reader(f, lineterminator = "\n")
            for row in reader:
                if row[1] == "XBTUSD" and row[0] != "timestamp":
                    bitmex.append(row)
        liquid = []
        with open(f"./csv_files/liquid_BTCUSD_{file_date}.csv","r") as f:
            reader = csv.reader(f, lineterminator = "\n")
            for row in reader:
                liquid.append(row)

        def close_price_find(execution,correct_time):
            count = 0
            for one_exec in execution:
                this_time = one_exec[0][:19]
                this_datetime = datetime.strptime(this_time,'%Y-%m-%d %H:%M:%S')
                if this_datetime < correct_time:
                    return_exec = one_exec[1]
                    count += 1
                else:
                    break 
            del execution[0:count-1] 
            return return_exec,execution

        def close_price_find_bitmex(execution,correct_time):
            count = 0
            for one_exec in execution:
                this_time = one_exec[0][:10]+" " + one_exec[0][11:19]
                this_datetime = datetime.strptime(this_time,'%Y-%m-%d %H:%M:%S')
                if this_datetime <= correct_time:
                    return_exec = one_exec[4]
                    count += 1
                else:
                    break 
            del execution[0:count-1] 
            return return_exec,execution
        
        def bitmex_volume(execution,correct_time):
            one_second_volume = 0
            for one_exec in execution:
                this_time = one_exec[0][:10]+" " + one_exec[0][11:19]
                this_datetime = datetime.strptime(this_time,'%Y-%m-%d %H:%M:%S')
                if correct_time <this_time and correct_time+ timedelta(seconds = 1) > this_time:
                    one_second_volume += one_exec[3]
            return one_second_volume

        flag = True
        now_string = bitmex[0][0][:10]+ " " + bitmex[0][0][11:19]
        now = datetime.strptime(now_string,'%Y-%m-%d %H:%M:%S')
        graph_bmx_usd = []
        graph_lqd_usd = []
        bitmex_volume = []
        graph_axis_time = []
        graph_time = now + timedelta(hours = 2)
        all_trade_exec =[]
        counter = 0
        graph_counter = 1
        while flag:
            print(now)
            bitmex_one_exec,bitmex = close_price_find_bitmex(bitmex,now)
            liquid_one_exec,liquid = close_price_find(liquid,now)
            one_bitmex_volume = bitmex_volume(bitmex,now)
            bitmex_one_exec = float(bitmex_one_exec)
            all_trade_exec.append([now,bitmex_one_exec,one_bitmex_volume])
            if counter == 0:
                graph_bmx_usd = [float(bitmex_one_exec)]
                graph_lqd_usd = [float(liquid_one_exec)]
                bitmex_volume = [one_bitmex_volume]
                graph_axis_time = [now]
            else:
                graph_bmx_usd.append(float(bitmex_one_exec))
                graph_lqd_usd.append(float(liquid_one_exec))
                bitmex_volume.append(one_bitmex_volume)
                graph_axis_time.append(now)
            now = now + timedelta(seconds = 1)
            counter += 1
            if counter % 1000 == 0:
                with open(f"./csv_files/all_trade_data_USD_{str(now)[:4]+str(now)[5:7]+str(now)[8:10]}.csv","a") as f:
                    writer = csv.writer(f,lineterminator="\n")
                    writer.writerows(all_trade_exec)
            if graph_time < now:
                fig = plt.figure()
                ax = fig.add_subplot(2, 1, 1)

                # plot
                ax.plot(graph_axis_time, graph_bmx_usd, color='b', label='bitmex BTCUSD')
                ax.plot(graph_axis_time, graph_lqd_usd, color='#e46409', label='liquid BTCJPY')

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
                plt.savefig(f"./graphs/bitmexcsv_USD_{str(now)[:4]+str(now)[5:7]+str(now)[8:10]}_{graph_counter}.png")
                graph_bmx_usd = [float(bitmex_one_exec)]
                graph_axis_time = [now]
                graph_time = now + timedelta(hours = 2)
                graph_counter += 1
                plt.close()
                all_trade_exec = []
                bitmex_volume = []
            if len(bitmex) < 5:
                flag = False

if __name__ == "__main__":
    now = datetime.now(timezone("Asia/Tokyo"))
    now = now.replace(hour=0,minute=0,second=0,microsecond=0)
    yesterday = now-timedelta(days = 1)
    parser = parse()
    parser.run()
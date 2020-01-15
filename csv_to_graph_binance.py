import csv 
from datetime import datetime, timezone, timedelta
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import os


class binance_graph():
    def output_graph(self,yesterday):
        file_date = str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]
        binance = []
        
        with open(f"./csv_files/binance_BTCUSDT_{file_date}.csv","r") as f:
            reader = csv.reader(f, lineterminator = "\n")
            for row in reader:
                binance.append(row)
        binance.reverse()

        def close_price_find(execution,correct_time):
            count = 0
            for one_exec in execution:
                this_time = one_exec[0][:19]
                this_datetime = datetime.strptime(this_time,'%Y-%m-%d %H:%M:%S')
                if this_datetime <= correct_time:
                    return_exec = one_exec[1]
                    count += 1
                else:
                    break 
            del execution[0:count-1] 
            return return_exec,execution

        continue_flag = True
        now_string = binance[0][0][:10]+ " " + binance[0][0][11:19]
        now = datetime.strptime(now_string,'%Y-%m-%d %H:%M:%S')
        graph_binance_usd = []
        graph_axis_time = []
        graph_time = now + timedelta(hours = 1)
        all_trade_exec =[]
        counter = 0
        graph_counter = 1
        while continue_flag:
            binance_one_exec,binance = close_price_find(binance,now)
            all_trade_exec.append([now,binance_one_exec])
            if counter == 0:
                graph_binance_usd = [float(binance_one_exec)]
                graph_axis_time = [now]
            else:
                graph_binance_usd.append(float(binance_one_exec))
                graph_axis_time.append(now)
            now = now + timedelta(seconds = 1)
            counter += 1
            if graph_time < now:
                plt.plot(graph_axis_time,graph_binance_usd)

                # save as png
                plt.savefig(f"./graphs/binance_USD_{str(now)[:4]+str(now)[5:7]+str(now)[8:10]}_{graph_counter}.png")
                graph_binance_usd = [float(binance_one_exec)]
                graph_axis_time = [now]
                graph_time = now + timedelta(hours = 1)
                graph_counter += 1
                plt.close()
            if len(binance) < 5:
                continue_flag = False

if __name__ == "__main__":
    now = datetime.now()
    yesterday = now-timedelta(hours = 1)
    parser = binance_graph()
    parser.run(yesterday)
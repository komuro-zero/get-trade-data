import csv 
from datetime import datetime, timezone, timedelta
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import os


class JPY_csv_to_graph():
    def run(self,yesterday):
        file_date = str(yesterday)[:4]+str(yesterday)[5:7]+str(yesterday)[8:10]
        btf = []
        btf_fx = []
        lqd = []

        with open(f"./csv_files/bitflyer_BTC_JPY_{file_date}.csv","r") as f:
            reader = csv.reader(f, lineterminator = "\n")
            for row in reader:
                btf.append(row)
        
        with open(f"./csv_files/bitflyer_FX_BTC_JPY_{file_date}.csv","r") as f:
            reader = csv.reader(f, lineterminator = "\n")
            for row in reader:
                btf_fx.append(row)

        with open(f"./csv_files/liquid_BTCJPY_{file_date}.csv","r") as f:
            reader = csv.reader(f, lineterminator = "\n")
            for row in reader:
                if row[1] == "XBTUSD" and row[0] != "timestamp":
                    lqd.append(row)
       

        def close_price_find(execution,correct_time):
            count = 0
            return_exec = 0
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
        

        flag = True
        now_string = btf[0][0][:10]+ " " + btf[0][0][11:19]
        now = datetime.strptime(now_string,'%Y-%m-%d %H:%M:%S')
        graph_btf_jpy = []
        graph_btf_fx_jpy = []
        graph_lqd_jpy = []
        graph_axis_time = []
        graph_time = now + timedelta(hours = 1)
        all_trade_exec =[]
        counter = 0
        graph_counter = 1
        while flag:
            print(now)
            bitflyer_one_exec,btf = close_price_find(btf,now)
            bitflyer_fx_one_exec,btf_fx = close_price_find(btf_fx,now)
            liquid_one_exec,lqd = close_price_find(lqd,now)
            all_trade_exec.append([now,bitflyer_one_exec,bitflyer_fx_one_exec,liquid_one_exec])
            if counter == 0:
                graph_btf_jpy = [float(bitflyer_one_exec)]
                graph_btf_fx_jpy = [float(bitflyer_fx_one_exec)]
                graph_lqd_jpy = [float(liquid_one_exec)]
                graph_axis_time = [now]
            else:
                graph_btf_jpy.append(float(bitflyer_one_exec))
                graph_btf_fx_jpy.append(float(bitflyer_fx_one_exec))
                graph_lqd_jpy.append(float(liquid_one_exec))
                graph_axis_time.append(now)
            now = now + timedelta(seconds = 1)
            counter += 1
            if counter % 1000 == 0:
                with open(f"./csv_files/all_trade_data_JPY_{str(now)[:4]+str(now)[5:7]+str(now)[8:10]}.csv","a") as f:
                    writer = csv.writer(f,lineterminator="\n")
                    writer.writerows(all_trade_exec)
                all_trade_exec = []
            if graph_time < now:

                # plot
                plt.plot(graph_axis_time, graph_btf_jpy, color='b', label='bitflyer BTCJPY')
                plt.plot(graph_axis_time, graph_btf_fx_jpy, color='y', label='bitflyer fx BTCJPY')
                plt.plot(graph_axis_time, graph_lqd_jpy, color='g', label='liquid BTCJPY')

                # x axis
                #plt.locator_params(axis='x', nbins=5)
                plt.xlabel('time')

                # y axis
                plt.ylabel('price JPY')

                # legend and title
                plt.legend(loc='best')
                plt.title(f'BTCJPY {now}')
                os.makedirs("./graphs/", exist_ok=True)


                # save as png
                plt.savefig(f"./graphs/BTCJPY_{str(now)[:4]+str(now)[5:7]+str(now)[8:10]}_{graph_counter}.png")
                graph_btf_jpy = [float(bitflyer_one_exec)]
                graph_btf_fx_jpy = [float(bitflyer_fx_one_exec)]
                graph_lqd_jpy = [float(liquid_one_exec)]
                graph_axis_time = [now]
                graph_time = now + timedelta(hours = 1)
                graph_counter += 1
                plt.close()
            if len(btf) < 5:
                flag = False

if __name__ == "__main__":
    now = datetime.now(timezone("Asia/Tokyo"))
    now = now.replace(hour=0,minute=0,second=0,microsecond=0)
    yesterday = now-timedelta(days = 1)
    parser = JPY_csv_to_graph()
    # parser.run()
import csv 
from datetime import datetime, timezone, timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import os


class parse():
    def run(self):
        file_date = datetime.now()
        bitflyer = []
        temp_bitflyer = []
        with open(f"./csv_files/bitflyer_BTCJPY_{str(file_date)[:4]+str(file_date)[5:7]+str(file_date)[8:10]}.csv","r") as f:
            reader = csv.reader(f, lineterminator = "\n")
            for row in reader:
                temp_bitflyer.append(row)
        #rearrange bitflyer to be old to new
        for i in range(1,len(temp_bitflyer)):
            bitflyer.append(temp_bitflyer[-i])

        liquid_USD = []
        with open(f"./csv_files/liquid_BTCUSD_{str(file_date)[:4]+str(file_date)[5:7]+str(file_date)[8:10]}.csv","r") as f:
            reader = csv.reader(f, lineterminator = "\n")
            for row in reader:
                liquid_USD.append(row)

        liquid = []
        with open(f"./csv_files/liquid_BTCJPY_{str(file_date)[:4]+str(file_date)[5:7]+str(file_date)[8:10]}.csv","r") as f:
            reader = csv.reader(f, lineterminator = "\n")
            for row in reader:
                liquid.append(row)

        bitmex = []
        with open(f"./csv_files/bitmex_BTCUSD_{str(file_date)[:4]+str(file_date)[5:7]+str(file_date)[8:10]}.csv","r") as f:
            reader = csv.reader(f, lineterminator = "\n")
            for row in reader:
                bitmex.append(row)


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
            del execution[0:count-10] 
            return return_exec,execution


        start_time = datetime.now()
        start_time = start_time.replace(microsecond= 0)
        now = start_time - timedelta(days = 1)
        flag = True
        graph_btf_jpy = []
        graph_lqd_jpy = []
        graph_axis_time = []
        graph_time = now + timedelta(hours = 2)
        all_trade_exec =[]
        counter = 0
        graph_counter = 1
        while flag:
            bitflyer_one_exec,bitflyer = close_price_find(bitflyer,now)
            liquid_one_exec,liquid = close_price_find(liquid,now)
            all_trade_exec.append([now,bitflyer_one_exec,liquid_one_exec])
            if counter == 0:
                graph_btf_jpy = [float(bitflyer_one_exec)]
                graph_lqd_jpy = [float(liquid_one_exec)]
                graph_axis_time = [now]
            else:
                graph_btf_jpy.append(float(bitflyer_one_exec))
                graph_lqd_jpy.append(float(liquid_one_exec))
                graph_axis_time.append(now)
            now = now + timedelta(seconds = 1)
            counter += 1
            with open(f"./csv_files/all_trade_data_JPY_{str(start_time)[:4]+str(start_time)[5:7]+str(start_time)[8:10]}.csv","a") as f:
                writer = csv.writer(f,lineterminator="\n")
                writer.writerows(all_trade_exec)
            if graph_time < now:
                fig = plt.figure()
                ax = fig.add_subplot(1, 1, 1)

                # plot
                ax.plot(graph_axis_time, graph_btf_jpy, color='b', label='bitflyer BTCJPY')
                ax.plot(graph_axis_time, graph_lqd_jpy, color='#e46409', label='liquid BTCJPY')

                # x axis
                #plt.locator_params(axis='x', nbins=5)
                ax.set_xlabel('time')

                # y axis
                ax.set_ylabel('price JPY')

                # legend and title
                ax.legend(loc='best')
                ax.set_title(f'bitflyer liquid JPY {now}')
                os.makedirs("./graphs/", exist_ok=True)

                # save as png
                date = str(start_time)[:4]+str(start_time)[5:7]+str(start_time)[8:10]
                path = f'./graphs/btf_lqd_{date}_{graph_counter}.png'
                plt.savefig(path)
                graph_time = now + timedelta(hours = 2)
                graph_axis_time = [now]
                graph_btf_jpy = [float(bitflyer_one_exec)]
                graph_lqd_jpy = [float(liquid_one_exec)]
                graph_counter += 1
                plt.close()
            all_trade_exec = []
            if start_time < now:
                flag = False

        start_time = datetime.now()
        start_time = start_time.replace(microsecond= 0)
        now = start_time - timedelta(days = 1)
        flag = True
        graph_bmx_usd = []
        graph_lqd_usd = []
        graph_axis_time = []
        graph_time = now + timedelta(hours = 2)
        all_trade_exec =[]
        counter = 0
        graph_counter = 1
        while flag:
            bitmex_one_exec,bitmex = close_price_find(bitmex,now)
            bitmex_one_exec = float(bitmex_one_exec)
            liquid_USD_one_exec,liquid_USD = close_price_find(liquid_USD,now)
            all_trade_exec.append([now,bitmex_one_exec,liquid_USD_one_exec])
            if counter == 0:
                graph_bmx_usd = [float(bitmex_one_exec)]
                graph_lqd_usd = [float(liquid_USD_one_exec)]
                graph_axis_time = [now]
            else:
                graph_bmx_usd.append(float(bitmex_one_exec))
                graph_lqd_usd.append(float(liquid_USD_one_exec))
                graph_axis_time.append(now)
            now = now + timedelta(seconds = 1)
            counter += 1
            if counter % 1000 == 0:
                print("iteration:",counter)
            with open(f"./csv_files/all_trade_data_USD_{str(start_time)[:4]+str(start_time)[5:7]+str(start_time)[8:10]}.csv","a") as f:
                writer = csv.writer(f,lineterminator="\n")
                writer.writerows(all_trade_exec)
            if graph_time < now:
                fig = plt.figure()
                ax = fig.add_subplot(1, 1, 1)

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
                ax.set_title(f'bitmex liquid USD {now}')
                os.makedirs("./graphs/", exist_ok=True)
                # save as png
                path2 = f'./graphs/bmx_lqd_{date}_{graph_counter}.png'
                plt.savefig(path2)
                graph_bmx_usd = [float(bitmex_one_exec)]
                graph_lqd_usd =[float(liquid_USD_one_exec)]
                graph_axis_time = [now]
                graph_time = now + timedelta(hours = 2)
                graph_counter += 1
                plt.close()
            all_trade_exec = []
            if start_time < now:
                flag = False
# This script runs the trading strategy
import pandas as pd

# True if strat should use 2 from each side to long short. False if to take only 1
USE_TOP_BOTTOM_2 = False

df = pd.read_csv('merged_file.csv')

df['AFRM_adj_1_change_pred'] = df['AFRM_adj_1_change_pred'].ffill()
df['AFRM_adj_1_change_pred'] = df['AFRM_adj_1_change_pred'].bfill()
df['UPST_adj_1_change_pred'] = df['UPST_adj_1_change_pred'].ffill()
df['UPST_adj_1_change_pred'] = df['UPST_adj_1_change_pred'].bfill()
df['SOFI_adj_1_change_pred'] = df['SOFI_adj_1_change_pred'].ffill()
df['SOFI_adj_1_change_pred'] = df['SOFI_adj_1_change_pred'].bfill()
df['LC_adj_1_change_pred'] = df['LC_adj_1_change_pred'].ffill()
df['LC_adj_1_change_pred'] = df['LC_adj_1_change_pred'].bfill()
df['OPRT_adj_1_change_pred'] = df['OPRT_adj_1_change_pred'].ffill()
df['OPRT_adj_1_change_pred'] = df['OPRT_adj_1_change_pred'].bfill()

df['long_gain'] = 0
df['short_gain'] = 0
df['daily_return'] = 0
df['daily_return_eventful_days'] = 0

for index, row in df.iterrows():

    actual = {
        'AFRM_adj_1_change': row['AFRM_adj_1_change'],

        'LC_adj_1_change': row['LC_adj_1_change'],

        'OPRT_adj_1_change': row['OPRT_adj_1_change'],

        'SOFI_adj_1_change': row['SOFI_adj_1_change'],

        'UPST_adj_1_change': row['UPST_adj_1_change'],
    }

    predicted = {
        'AFRM_adj_1_change_pred': row['AFRM_adj_1_change_pred'],

        'LC_adj_1_change_pred': row['LC_adj_1_change_pred'],

        'OPRT_adj_1_change_pred': row['OPRT_adj_1_change_pred'],

        'SOFI_adj_1_change_pred': row['SOFI_adj_1_change_pred'],

        'UPST_adj_1_change_pred': row['UPST_adj_1_change_pred'],
    }

    sorted_d = sorted(predicted.items(), key=lambda x: x[1])

    # get 2 max
    max_key = sorted_d[-1][0]
    max_2_key = sorted_d[-2][0]

    # get 2 min
    min_key = sorted_d[0][0]
    min_2_key = sorted_d[1][0]

    # creating the strat assuming weights of 0.5 -0.5
    print(index)
    if USE_TOP_BOTTOM_2:
        df.loc[index, 'long_gain'] = 0.25 * (actual[max_key[:-5]]) + 0.25 * (actual[max_2_key[:-5]])
        df.loc[index, 'short_gain'] = -0.25 * (actual[min_key[:-5]]) - 0.25 * (actual[min_2_key[:-5]])
    else:
        df.loc[index, 'long_gain'] = 0.5 * (actual[max_key[:-5]])
        df.loc[index, 'short_gain'] = -0.5 * (actual[min_key[:-5]])

    df.loc[index, 'daily_return'] = df.loc[index, 'long_gain'] + df.loc[index, 'short_gain']

    # Calculating only trading on days that there's a change
    try:
        if df.loc[index, 'AFRM_adj_1_change_pred'] != df.loc[index - 1, 'AFRM_adj_1_change_pred'] \
                or df.loc[index, 'LC_adj_1_change_pred'] != df.loc[index - 1, 'LC_adj_1_change_pred'] \
                or df.loc[index, 'OPRT_adj_1_change_pred'] != df.loc[index - 1, 'OPRT_adj_1_change_pred'] \
                or df.loc[index, 'SOFI_adj_1_change_pred'] != df.loc[index - 1, 'SOFI_adj_1_change_pred'] \
                or df.loc[index, 'UPST_adj_1_change_pred'] != df.loc[
            index - 1, 'UPST_adj_1_change_pred']:  # Days without change will have 1 return meaning we do not trade there
            df.loc[index, 'daily_return_eventful_days'] = df.loc[index, 'daily_return']
    except:
        print(f'index equals: {index}')

    print('end of one row iteration')

df['compounded_returns'] = (1 + df['daily_return']).cumprod() - 1
df['compounded_returns_eventful_days'] = (1 + df['daily_return_eventful_days']).cumprod() - 1
df['compounded_bench_returns'] = (1 + df['benchmark_avg_adj_1_change']).cumprod() - 1

import matplotlib.pyplot as plt

# df.plot(x='Date', y='daily_return_eventful_days', color='blue')
# df.plot(x='Date', y='daily_return', title='Cummulative returns per date', color='green')
# plt.show()
# df.to_csv('/Users/eyalben-eliyahu/Desktop/returns test.csv')

###strategy evaluation:

ev_d_ret = df.loc[df['Date'] == '2022-11-23', 'compounded_returns_eventful_days'].values[0]
all_d_ret = df.loc[df['Date'] == '2022-11-23', 'compounded_returns'].values[0]
benchmark_ret = df.loc[df['Date'] == '2022-11-23', 'compounded_bench_returns'].values[0]

ev_d_vector = df.loc[df['daily_return_eventful_days'] != 0, 'daily_return_eventful_days']
all_d_vector = df.loc[df['Date'] <= '2022-11-23', 'daily_return']
benchmark_vector = df.loc[df['Date'] <= '2022-11-23', 'benchmark_avg_adj_1_change']

ev_d_std = ev_d_vector.values.std()
all_d_std = all_d_vector.values.std()
benchmark_std = benchmark_vector.values.std()

ev_d_sharpe = ev_d_ret / ev_d_std
all_d_sharpe = all_d_ret / all_d_std
benchmark_sharpe = benchmark_ret / benchmark_std

ev_d_num_of_trades = len(ev_d_vector)
all_d_num_of_trades = len(all_d_vector)
benchmark_num_of_trades = len(benchmark_vector)

ev_d_annualized_ret_efficient = (1 + ev_d_ret)**(365/ev_d_num_of_trades) - 1 ## This assumes max efficiency in trading and capital, becasue it assumes other usage of capital in days not trading
ev_d_annualized_ret = (1 + ev_d_ret)**(365/benchmark_num_of_trades) - 1
all_d_annualized_ret = (1 + all_d_ret)**(365/all_d_num_of_trades) - 1
benchmark_annualized_ret = (1 + benchmark_ret)**(365/benchmark_num_of_trades) - 1



df['compounded_returns_eventful_days'].plot(label="eventful_days", color="green", xlabel='days',
                                            ylabel='compounded returns')
df['compounded_returns'].plot(label="every_day", color="blue")
df['compounded_bench_returns'].plot(label="benchmark", color="grey")
plt.text(250, 0.37, f"{round(ev_d_ret, 3) * 100}%", color="green")
plt.text(250, 0, f"{round(all_d_ret, 3) * 100}%", color="blue")
plt.text(250, -0.7, f"{round(benchmark_ret, 3) * 100}%", color="grey")
plt.legend()
plt.show()


def strategy_evaluation(ret, std, trades_vector, annualized_return, annualized_return_efficient, name):
    ##soratino_ratio =
    print(
        f"Strategy evaluation for {name}: Tot Return: {round(ret, 3)} | Annualized Return: {round(annualized_return,3)} | Annualized Return Efficient: {round(annualized_return_efficient,3)} | Volatility: {round(std, 3)} | Sharpe: {round(ret / std, 3)} | # trades: {len(trades_vector)} | Best Day: {round(max(trades_vector), 3)} | Worst Day {round(min(trades_vector), 3)}")



strategy_evaluation(ev_d_ret, ev_d_std, ev_d_vector, ev_d_annualized_ret, ev_d_annualized_ret_efficient, "Eventful ")
strategy_evaluation(all_d_ret, all_d_std, all_d_vector,all_d_annualized_ret , all_d_annualized_ret, "Everyday ")
strategy_evaluation(benchmark_ret, benchmark_std, benchmark_vector, benchmark_annualized_ret,benchmark_annualized_ret , "Benchmark")

print('end')

import matplotlib.pyplot as plt
import pandas as pd
import os

ticker_list = ["AFRM","LC","OPRT","SOFI","UPST"]

def plot_features_per_issuer(ticker, feature):
    directory = f"Output data/cohort stock/{ticker}"
    list_of_abss = []
    for filename in os.scandir(directory):
        if (filename.is_file()) and ("bench" in str(filename)):
            list_of_abss.append(str(filename.path))

    for file in list_of_abss:
        try:
            df = pd.read_csv(file)[feature]
            df.plot(title=f'{feature} for {ticker}',xlabel = "Months Old", ylabel=f"{feature}", color='black')
            plt.grid(color='grey', linestyle='--', linewidth=0.05)
        except:
            print(f"no {feature} for {ticker}")
    plt.show()
    # print(df)

for i in ticker_list:
    plot_features_per_issuer(i,"Life CDR")
    plot_features_per_issuer(i,"Life CPR")
    plot_features_per_issuer(i, "Annualized Net Loss Rate")
    plot_features_per_issuer(i, "Gross Coupon")

## To Do:
## Plot all the graphs, per feature, in one plot. Look for 'subplot' in matplot lib
## Plot also the result of (Annualized Net Loss Rate - Gross Coupon)
## Can find elegant way to subplot also the "Volatility graphs?"


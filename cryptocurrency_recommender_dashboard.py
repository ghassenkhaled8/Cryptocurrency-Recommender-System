START_DATE = "2021-01-01" # start date for historical data
RSI_TIME_WINDOW = 7 #number of days


import requests
import pandas as pd 
import warnings
import datetime as dt
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas_datareader.data as web
from plotly.subplots import make_subplots
warnings.filterwarnings('ignore')

## URLS and names
urls = ["https://www.cryptodatadownload.com/cdd/Bitfinex_EOSUSD_d.csv", 
        "https://www.cryptodatadownload.com/cdd/Bitfinex_EDOUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_BTCUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_ETHUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_LTCUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_BATUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_OMGUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_DAIUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_ETCUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_ETPUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_NEOUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_REPUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_TRXUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_XLMUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_XMRUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_XVGUSD_d.csv", 
       ]
crypto_names = ["EOS Coin (EOS)",
                "Eidoo (EDO)",
                "Bitcoin (BTC)",
                "Ethereum (ETH)",
                "Litecoin (LTC)",
                "Basic Attention Token (BAT)",
                "OmiseGO (OMG)",
                "Dai (DAI)",
                "Ethereum Classic (ETC)",
                "Metaverse (ETP)",
                "Neo (NEO)",
                "Augur (REP)",
                "TRON (TRX)",
                "Stellar (XLM)",
                "Monero (XMR)",
                "Verge (XVG)"
               ]

## Data download and loading 
def df_loader(urls , start_date = "2021-01-01"):
    filenames = []
    all_df = pd.DataFrame()
    for idx,url in enumerate(urls):
        req = requests.get(url,verify=False)
        url_content = req.content
        filename = url[48:]
        csv_file = open( filename , 'wb')
        csv_file.write(url_content)
        csv_file.close()
        filename = filename[:-9]
        filenames.append(filename)
    for file in filenames:
        df = pd.read_csv(file + "USD_d.csv", header = 1, parse_dates=["date"])
        df = df [df["date"] > start_date]
        df.index = df.date
        df.drop(labels = [df.columns[0],df.columns[1],df.columns[8]] , axis = 1 , inplace = True)
        all_df = pd.concat([all_df,df], ignore_index=False)

    return all_df , filenames 
def computeRSI (data, time_window):
    diff = data.diff(1).dropna()
    up_chg = 0 * diff
    down_chg = 0 * diff
    up_chg[diff > 0] = diff[ diff>0 ]
    down_chg[diff < 0] = diff[ diff < 0 ]
    up_chg_avg = up_chg.ewm(com=time_window-1, min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1, min_periods=time_window).mean()
    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi

all_df , filenames = df_loader(urls , start_date=START_DATE)

crypto_df = []
for file in filenames:
    symbol = file + str("/USD")
    temp_df = pd.DataFrame(all_df[all_df["symbol"] == symbol])
    temp_df.drop(columns= ["symbol"] ,inplace = True)
    temp_df["close_rsi"] = computeRSI(temp_df['close'], time_window=RSI_TIME_WINDOW)
    temp_df["high_rsi"] = 30
    temp_df["low_rsi"] = 70
    exec('%s = temp_df.copy()' % file.lower())
    crypto_df.append(temp_df)

## plot 
fig = make_subplots(rows=3, 
                    cols=2,
                    shared_xaxes=True,
                    specs=[[{"rowspan": 2}, {"rowspan": 2}], [{"rowspan": 1}, {"rowspan": 1}] , [{},{}]]
                    
                   )
date_buttons = [
{'step': "all", 'label': "All time"},
{'count':  1, 'step': "year", 'stepmode': "backward", 'label': "Last Year"},
{'count':  1, 'step': "year", 'stepmode': "todate", 'label': "Current Year"},
{'count':  1, 'step': "month", 'stepmode': "backward", 'label': "Last 2 Months"},
{'count':  1, 'step': "month", 'stepmode': "todate", 'label': "Current Month"},
{'count':  7, 'step': "day", 'stepmode': "todate", 'label': "Current Week"},
{'count':  4, 'step': "day", 'stepmode': "backward", 'label': "Last 4 days"},
{'count':  1, 'step': "day", 'stepmode': "backward", 'label': "Today"},
               ]
buttons = []
i = 0
j=0
COUNT = 8
vis = [False] * len(crypto_names) * COUNT
for df in crypto_df:
    for k in range(COUNT):
        vis[j+k] = True
    buttons.append({ 'label' : crypto_names[i],
                     'method' : 'update',
                     'args'   : [{'visible' : vis},
                                {'title'  : crypto_names[i] + ' Charts and Indicators'}
                                ] }
                  )
    i+=1
    j+=COUNT
    vis = [False] * len(crypto_names)* COUNT
for df in crypto_df:
    fig.add_trace(
        go.Candlestick(x= df.index,
                       open  = df['open'],
                       high  = df['high'],
                       low   = df['low'],
                       close = df['close'],
                       showlegend =False
                                ),
                  row=1, 
                  col=1)
    fig.add_trace(
        go.Bar(x =df.index ,
               y=df["Volume USD"],
               showlegend =False, 
               marker_color='aqua'),
        row=3, 
        col=1)
    fig.add_trace(
        go.Scatter(x=df.index, y=df['close'],
                   mode='lines',
                  showlegend =False,
                   line=dict(color="red", width=4)),
        row=1, 
        col=2)
    fig.add_trace(
        go.Scatter(x=df.index,
                   y=df['low'],
                   fill='tonexty',
                   mode='lines',
                   showlegend =False,                   
                   line=dict(width=2, color='pink', dash='dash')),
        row=1, 
        col=2)
    fig.add_trace(
        go.Scatter(x=df.index, 
                   y=df['high'],
                   fill='tonexty',
                   mode='lines',
                   showlegend =False, 
                   line=dict(width=2, color='pink', dash='dash')),
        row=1, 
        col=2)
    fig.add_trace(
        go.Scatter(x=df.index, y=df['close_rsi'],
                   mode='lines',
                  showlegend =False,
                   line=dict(color="aquamarine", width=4)),
        row=3, 
        col=2)
    fig.add_trace(
        go.Scatter(x=df.index,
                   y=df['low_rsi'],
                   fill='tonexty', 
                   mode='lines',
                   showlegend =False,                   
                   line=dict(width=2, color='aqua', dash='dash')),
        row=3, 
        col=2)
    fig.add_trace(
        go.Scatter(x=df.index, 
                   y=df['high_rsi'],
                   fill='tonexty',
                   mode='lines',
                   showlegend =False, 
                   line=dict(width=2, color='aqua', dash='dash')),
        row=3, 
        col=2)
    
    
fig.update_xaxes(
        tickfont = dict(size=15, family = 'monospace', color='#B8B8B8'),
        tickmode = 'array',
        ticklen = 6,
        showline = False,
        showgrid = True,
        gridcolor = '#595959',
        ticks = 'outside')
fig.update_layout(
    spikedistance=100, 
    xaxis_rangeslider_visible=False,
    hoverdistance=1000)
fig.update_xaxes(
    showspikes=True,  
    spikesnap="cursor",
    spikemode="across"
                )
fig.update_yaxes(
    showspikes=True, 
    spikesnap='cursor',
    spikemode="across"                 
                )
fig.update_yaxes(
        tickfont = dict(size=15, family = 'monospace', color='#B8B8B8'),
        tickmode = 'array',
        showline = False,
        ticksuffix = '$',
        showgrid = True,
        gridcolor = '#595959',
        ticks = 'outside')
fig.update_layout(
                  width=1120,
                  height=650,
                  font_family   = 'monospace',
                  xaxis         = dict(rangeselector = dict(buttons = date_buttons)),
                  updatemenus   = [dict(type = 'dropdown',
                                        x = 1.0,
                                        y = 1.108,
                                        showactive = True,
                                        active = 2,
                                        buttons = buttons)],
                  title         = dict(text = '<b>Cryptocurrencies  Dashboard<b>',
                                       font = dict(color = '#FFFFFF' ,size = 22), 
                                       x = 0.50),
                  font          = dict(color="blue"), 
                  annotations   = [
                                  dict( text = "<b>Choose Cryptocurrency: <b>",
                                        font = dict(size = 20 , color = "#ffffff"),
                                        showarrow=False,
                                        x = 1.02, 
                                        y = 1.20,
                                        xref = 'paper', yref = "paper",
                                        align = "left"),
                                  dict( text = "<b>Candlestick Chart <b>",
                                        font = dict(size = 20,  color = "#ffffff"),
                                        showarrow=False,
                                        x = 0.12, 
                                        y = 0.285,
                                        xref = 'paper', yref = "paper",
                                        align = "left"),
                                  dict( text = "<b>Price Chart<b>",
                                        font = dict(size = 20,  color = "#ffffff"),
                                        showarrow=False,
                                        x = 0.82, 
                                        y = 0.285,
                                        xref = 'paper', yref = "paper",
                                        align = "left"),
                                  dict( text = "<b>Volume Traded<b>",
                                        font = dict(size = 20,  color = "#ffffff"),
                                        showarrow=False,
                                        x = 0.14, 
                                        y = -0.53,
                                        xref = 'paper', yref = "paper",
                                        align = "left"),
                                  dict( text = "<b>Relative Strength Index (RSI)<b>",
                                        font = dict(size = 20,  color = "#ffffff"),
                                        showarrow=False,
                                        x = 0.94, 
                                        y = -0.53,
                                        xref = 'paper', yref = "paper",
                                        align = "left")
                  ],
                template= "plotly_dark"
                )    
for i in range(0,16*COUNT):
    fig.data[i].visible = False
for i in range(COUNT):
    fig.data[i].visible = True
fig.layout["xaxis"]["rangeslider"]["visible"] = False
fig.layout["xaxis2"]["rangeslider"]["visible"] = False
fig.layout["xaxis5"]["rangeslider"]["visible"] = True
fig.layout["xaxis6"]["rangeslider"]["visible"] = True
fig.layout["xaxis5"]["rangeslider"]["borderwidth"] = 4
fig.layout["xaxis6"]["rangeslider"]["borderwidth"] = 4
fig.layout["xaxis5"]["rangeslider"]["bordercolor"] = "aqua"
fig.layout["xaxis6"]["rangeslider"]["bordercolor"] = "aqua"
fig.layout["yaxis6"]["ticksuffix"] = ""
fig.layout["yaxis6"]["range"] = [10,100]
fig.show()

from bs4 import BeautifulSoup

def fetch_cryptocurrency_info(selected_crypto):
    crypto_symbol = filenames[crypto_names.index(selected_crypto)].split("_")[1].lower()
    url = f"https://coinmarketcap.com/currencies/{crypto_symbol}/"

    try:
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")

        # Extract relevant data
        price_element = soup.find("div", {"class": "priceValue___11gHJ"})
        price = price_element.text.strip() if price_element else "N/A"

        market_cap_element = soup.find("div", {"class": "statsValue___2iaoZ"})
        market_cap = market_cap_element.text.strip() if market_cap_element else "N/A"

        volume_element = soup.find("div", {"class": "statsValue___2iaoZ"})
        volume = volume_element.text.strip() if volume_element else "N/A"

        return {
            "Price": price,
            "Market Cap": market_cap,
            "24h Volume": volume,
        }

    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return None

def cryptocurrency_chatbot():
    while True:
        print("\nChoose a cryptocurrency from the list:")
        for i, crypto_name in enumerate(crypto_names):
            print(f"{i+1}. {crypto_name}")

        print("0. Exit")
        choice = input("Enter the number of the cryptocurrency or 0 to exit: ")

        if choice == "0":
            print("Exiting the chatbot. Goodbye!")
            break
        elif choice.isdigit() and 0 < int(choice) <= len(crypto_names):
            selected_crypto = crypto_names[int(choice) - 1]
            index = crypto_names.index(selected_crypto)
            print(f"\nYou selected: {selected_crypto}")
            print("Here's some basic information:")
            print(f"Symbol: {filenames[index]}USD")
            print(f"Start Date: {START_DATE}")
            print(f"RSI Time Window: {RSI_TIME_WINDOW} days")
            
            # Fetch additional data from the internet
            crypto_info = fetch_cryptocurrency_info(selected_crypto)
            if crypto_info:
                print("\nReal-time information:")
                for key, value in crypto_info.items():
                    print(f"{key}: {value}")
            else:
                print("Failed to fetch real-time information.")
                
            print("\nOther data and insights can be found in the dashboard.")
        else:
            print("Invalid input. Please choose a valid option.")

# Start the chatbot
cryptocurrency_chatbot()


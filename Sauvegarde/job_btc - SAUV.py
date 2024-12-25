from prefect import flow,task

import json
import time
import requests
import sqlite3
import pandas as pd


## REQUEST
#Obtenir le prix actuel de toutes les crypto-monnaies dans toutes les autres devises prises en charge dont vous avez besoin.


response_5 = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Clitecoin&vs_currencies=eur%2Cusd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true&precision=2")
simple_price = response_5.json()

## PARSE
@task
def parse_api_coingecko():
    for dict in simple_price["bitcoin"]:
        eur = simple_price["bitcoin"]["eur"]
        eur_market_cap = simple_price["bitcoin"]["eur_market_cap"]
        eur_24h_vol = simple_price["bitcoin"]["eur_24h_vol"]
        eur_24h_change = simple_price["bitcoin"]["eur_24h_change"]
        usd = simple_price["bitcoin"]["usd"]
        usd_market_cap = simple_price["bitcoin"]["usd_market_cap"]
        usd_24h_vol = simple_price["bitcoin"]["usd_24h_vol"]
        usd_24h_change = simple_price["bitcoin"]["usd_24h_change"]
        last_updated_at = simple_price["bitcoin"]["last_updated_at"] 
        
        ## Transformation = colonne last_updated_at UNIXTIME
        last_updated_unix = time.localtime(last_updated_at)
        last_update_1 = time.strftime("%Y-%m-%d %H:%M:%S", last_updated_unix) 
        #print('euro:',eur,"\n"'dollar:',usd,"\n"'capitalisation boursiere €:',eur_market_cap,"\n"'Volume de négociation sur 24 h:',eur_24h_vol,"\n"'derniere Maj Prix:',last_updated_1)
         
        ## INSERT
        # CONNEXION BDD
        conn = sqlite3.connect("/GIT/Api/api_coingecko/ProjectBTC.db")
        cur = conn.cursor()
        req1 = 'INSERT INTO btc(eur,usd,last_update,eur_market_cap,eur_24h_vol) VALUES(?,?,?,?,?)'
        val1 = (eur,usd,last_update_1,eur_market_cap,eur_24h_vol)
        cur.execute(req1,val1)
        conn.commit() 
        conn.close()
        return (eur, usd, eur_market_cap, eur_24h_vol,last_update_1)



# parse_api_coingecko()


@task
def df_btc():
    
    # DATAFRAME
    conn = sqlite3.connect("/GIT/Api/api_coingecko/ProjectBTC.db")
    cur = conn.cursor()
    # df_btc = pd.read_sql('select eur,usd,last_update,eur_market_cap,eur_24h_vol from btc order by last_update',conn,)
    df_btc = pd.read_sql('''select * from btc WHERE DATE(last_update) = DATE('now')''',conn,)
    # SUPPRESSION DE DOUBLON => df_btc
    df_btc_no_duplicated = df_btc.drop_duplicates()
    
    return df_btc_no_duplicated

# df_btc = df_btc()

# VISU
@task
def visu(df_btc_no_duplicated):
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    fig = make_subplots(
    rows=4, cols=1,
    subplot_titles=("BTC euro", "BTC dollar","Capitalisation boursière","volume d'échange eur 24h"))

# Update xaxis properties
    fig.update_xaxes(title_text="Last update", row=1, col=1)
# Update yaxis properties
    fig.update_yaxes(title_text="euro", row=1, col=1)

# Update xaxis properties
    fig.update_xaxes(title_text="Last update", row=2, col=1)
# Update yaxis properties
    fig.update_yaxes(title_text="dollar", row=2, col=1)

# Update xaxis properties
    fig.update_xaxes(title_text="Last update", row=2, col=1)
# Update yaxis properties
    fig.update_yaxes(title_text="eur_market_cap", row=2, col=1)

# Update xaxis properties
    fig.update_xaxes(title_text="Last update", row=2, col=1)
# Update yaxis properties
    fig.update_yaxes(title_text="eur_24h_vol", row=2, col=1)

    fig.append_trace(go.Scatter(
    x = df_btc_no_duplicated["last_update"],
    y = df_btc_no_duplicated["eur"],
    name="cours BTC euro"
    ), row=1, col=1)

    fig.append_trace(go.Scatter(
    x = df_btc_no_duplicated["last_update"],
    y = df_btc_no_duplicated["usd"],
    name="cours BTC dollar"
    ), row=2, col=1)

    fig.append_trace(go.Scatter(
    x = df_btc_no_duplicated["last_update"],
    y = df_btc_no_duplicated["eur_market_cap"],
    name="capitalisation boursière"
    ), row=3, col=1)

    fig.append_trace(go.Scatter(
    x = df_btc_no_duplicated["last_update"],
    y = df_btc_no_duplicated["eur_24h_vol"],
    name="Volume de négociation sur 24 h"
    ), row=4, col=1)

    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(height=1200, width=1000, title_text="Evolution du cours du Bitcoin", hovermode = "x unified" )
    fig.write_html("/GIT/Api/api_coingecko/btc_eur_usd_DEX_24h.html")



@flow(name="BTC Info", log_prints=True)    
def btc_info():
    btc_info = parse_api_coingecko()
    df_btc_no_duplicated = df_btc()
    no_duplicated = visu(df_btc_no_duplicated)
   
if __name__ == "__main__":
    # Call a flow function for a local flow run!
    btc_info()

btc_info.visualize()
    
from prefect import flow,task
from prefect.deployments import Deployment
from prefect import flow
from prefect_email import EmailServerCredentials, email_send_message

import json
import time
import requests
import sqlite3
import pandas as pd


## REQUEST
#Obtenir le prix actuel de toutes les crypto-monnaies dans toutes les autres devises prises en charge.
@task
def request():
    response_5 = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Clitecoin&vs_currencies=eur%2Cusd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true&precision=2")
    simple_price = response_5.json()
    return simple_price

## PARSE
## PARSE
@task(viz_return_value=[1, 2, 3, 4, 5])
def parse_api_coingecko(simple_price):
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
        
    return eur,usd,eur_24h_vol,eur_market_cap,last_updated_at

@task
def transfo(last_updated_at):
    last_update_1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_updated_at)) 
    return last_update_1

## INSERT
# CONNEXION BDD
@task 
def insert(eur,usd,last_update_1,eur_market_cap,eur_24h_vol):
    conn = sqlite3.connect("/GIT/Api/api_coingecko/ProjectBTC.db")
    cur = conn.cursor()
    req1 = 'INSERT INTO btc(eur,usd,last_update,eur_market_cap,eur_24h_vol) VALUES(?,?,?,?,?)'
    val1 = (eur,usd,last_update_1,eur_market_cap,eur_24h_vol)
    cur.execute(req1,val1)
    conn.commit() 
    conn.close()
    return (eur, usd, eur_market_cap, eur_24h_vol,last_update_1)   

# DATAFRAME
@task
def df_btc():
    conn = sqlite3.connect("/GIT/Api/api_coingecko/ProjectBTC.db")
    cur = conn.cursor()
    # df_btc = pd.read_sql('select eur,usd,last_update,eur_market_cap,eur_24h_vol from btc order by last_update',conn,)
    df_btc = pd.read_sql('''select * from btc WHERE DATE(last_update) = DATE('now')''',conn,)
    # SUPPRESSION DE DOUBLON => df_btc
    df_btc_no_duplicated = df_btc.drop_duplicates()
    
    return df_btc_no_duplicated

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
    simple_price = request()
    #last_updated_at = parse_api_coingecko()
    eur,usd,eur_24h_vol,eur_market_cap,last_updated_at = parse_api_coingecko(simple_price)
    last_updated_1 =  transfo(last_updated_at)
    insertion = insert(eur, usd, last_updated_1, eur_market_cap, eur_24h_vol)
    df_btc_no_duplicated = df_btc()
    no_duplicated = visu(df_btc_no_duplicated)


def deploy():
    deployment = Deployment.build_from_flow(
        flow=btc_info,
        name="btc_info-deployment"
    )
    deployment.apply()
    
if __name__ == "__main__":
    # Call a flow function for a local flow run!
    deploy()
    
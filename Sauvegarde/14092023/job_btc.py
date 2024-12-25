from prefect import flow,task
from prefect import flow
#from prefect_email import EmailServerCredentials

import json
import time
import requests
import sqlite3
import pandas as pd


## REQUEST
#Obtenir le prix actuel de toutes les crypto-monnaies dans toutes les autres devises prises en charge.
@task
def request():
    response_5 = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Clitecoin%2Cethereum&vs_currencies=eur%2Cusd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true&precision=2")
    simple_price = response_5.json()
    return simple_price

## PARSE
@task(viz_return_value=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
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
        
        ltc_eur = simple_price["litecoin"]["eur"]
        ltc_eur_market_cap = simple_price["litecoin"]["eur_market_cap"]
        ltc_eur_24h_vol = simple_price["litecoin"]["eur_24h_vol"]
        ltc_eur_24h_change = simple_price["litecoin"]["eur_24h_change"]
        ltc_usd = simple_price["litecoin"]["usd"]
        ltc_usd_market_cap = simple_price["litecoin"]["usd_market_cap"]
        ltc_usd_24h_vol = simple_price["litecoin"]["usd_24h_vol"]
        ltc_usd_24h_change = simple_price["litecoin"]["usd_24h_change"]
        ltc_last_updated_at = simple_price["litecoin"]["last_updated_at"]
    
        eth_eur = simple_price["ethereum"]["eur"]
        eth_eur_market_cap = simple_price["ethereum"]["eur_market_cap"]
        eth_eur_24h_vol = simple_price["ethereum"]["eur_24h_vol"]
        eth_eur_24h_change = simple_price["ethereum"]["eur_24h_change"]
        eth_usd = simple_price["ethereum"]["usd"]
        eth_usd_market_cap = simple_price["ethereum"]["usd_market_cap"]
        eth_usd_24h_vol = simple_price["ethereum"]["usd_24h_vol"]
        eth_usd_24h_change = simple_price["ethereum"]["usd_24h_change"]
        eth_last_updated_at = simple_price["ethereum"]["last_updated_at"]
        
    return eur, usd, eur_24h_vol, eur_market_cap, last_updated_at, ltc_eur, ltc_usd, ltc_eur_24h_vol, ltc_eur_market_cap, ltc_last_updated_at, eth_eur, eth_usd, eth_eur_24h_vol, eth_eur_market_cap, eth_last_updated_at

@task(viz_return_value=[1, 2, 3])
def transfo(last_updated_at,ltc_last_updated_at,eth_last_updated_at):
    last_update_1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_updated_at))
    ltc_last_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ltc_last_updated_at))
    eth_last_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(eth_last_updated_at))   
    
    return last_update_1,ltc_last_updated,eth_last_updated


## INSERT
# CONNEXION BDD
@task 
def insert(eur,usd,last_update_1,eur_market_cap,eur_24h_vol,ltc_eur,ltc_usd,ltc_eur_24h_vol,ltc_eur_market_cap,ltc_last_updated,eth_eur,eth_usd,eth_eur_24h_vol,eth_eur_market_cap,eth_last_updated):
    # conn = sqlite3.connect("/git/Api/api_coingecko/ProjectBTC.db") # windows 
    conn = sqlite3.connect("/home/FBO/git/Api/api_coingecko/ProjectBTC.db") # Linux
    cur = conn.cursor()
    req_btc = 'INSERT INTO btc(eur,usd,last_update,eur_market_cap,eur_24h_vol) VALUES(?,?,?,?,?)'
    val_btc = (eur,usd,last_update_1,eur_market_cap,eur_24h_vol)
    req_ltc = 'INSERT INTO ltc(eur,usd,last_update,eur_market_cap,eur_24h_vol) VALUES(?,?,?,?,?)'
    val_ltc = (ltc_eur,ltc_usd,ltc_last_updated,ltc_eur_market_cap,ltc_eur_24h_vol)
    req_eth = 'INSERT INTO eth(eur,usd,last_update,eur_market_cap,eur_24h_vol) VALUES(?,?,?,?,?)'
    val_eth = (eth_eur,eth_usd,eth_last_updated,eth_eur_market_cap,eth_eur_24h_vol)
    cur.execute(req_btc,val_btc)
    cur.execute(req_ltc,val_ltc)
    cur.execute(req_eth,val_eth)
    conn.commit() 
    conn.close()
    #return eur, usd, eur_market_cap, eur_24h_vol, last_update_1, ltc_eur, ltc_usd, ltc_eur_24h_vol, ltc_eur_market_cap, ltc_last_updated, eth_eur, eth_usd, eth_eur_24h_vol, eth_eur_market_cap, eth_last_updated

# DATAFRAME
@task(viz_return_value=[1, 2, 3])
def dataframe():
    #conn = sqlite3.connect("/GIT/Api/api_coingecko/ProjectBTC.db") # Windows
    conn = sqlite3.connect("/home/FBO/git/Api/api_coingecko/ProjectBTC.db") # Linux
    cur = conn.cursor()
    # df_btc = pd.read_sql('select eur,usd,last_update,eur_market_cap,eur_24h_vol from btc order by last_update',conn,)
    df_btc = pd.read_sql('''select * from btc WHERE DATE(last_update) = DATE('now')''',conn,)
    df_ltc = pd.read_sql('''select * from ltc WHERE DATE(last_update) = DATE('now')''',conn,)
    df_eth = pd.read_sql('''select * from eth WHERE DATE(last_update) = DATE('now')''',conn,)
    
    # SUPPRESSION DE DOUBLON => df_btc
    df_btc_no_duplicated = df_btc.drop_duplicates(subset='last_update')
    df_ltc_no_duplicated = df_ltc.drop_duplicates(subset='last_update')
    df_eth_no_duplicated = df_eth.drop_duplicates(subset='last_update')
    
    return df_btc_no_duplicated,df_ltc_no_duplicated,df_eth_no_duplicated

# LAST VALUE
@task(viz_return_value=[1, 2, 3, 4, 5, 6])
def last_value(df_btc_no_duplicated,df_ltc_no_duplicated,df_eth_no_duplicated):
    
    # Dernière valeur = > btc
    derniere_valeur_btc = df_btc_no_duplicated['eur'].iloc[-1]
    derniere_valeur_btc_usd = df_btc_no_duplicated['usd'].iloc[-1]
    # Dernière valeur = > ltc
    derniere_valeur_ltc = df_ltc_no_duplicated['eur'].iloc[-1]
    derniere_valeur_ltc_usd = df_ltc_no_duplicated['usd'].iloc[-1]
    # Dernière valeur = > eth
    derniere_valeur_eth = df_eth_no_duplicated['eur'].iloc[-1]
    derniere_valeur_eth_usd = df_eth_no_duplicated['usd'].iloc[-1]
    
    return derniere_valeur_btc, derniere_valeur_btc_usd,derniere_valeur_ltc,derniere_valeur_ltc_usd,derniere_valeur_eth,derniere_valeur_eth_usd

# VISU
@task(viz_return_value=[1, 2, 3])
def visu_btc(df_btc_no_duplicated,derniere_valeur_btc, derniere_valeur_btc_usd):
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    fig = make_subplots(
    rows=5, cols=1,
    subplot_titles=("RSI","BTC euro", "BTC dollar","Capitalisation boursière","volume d'échange eur 24h"))

#  Propriétés axis RSI row=1, col=1
    fig.update_xaxes(title_text="Last update", row=1, col=1)
    fig.update_yaxes(title_text="RSI", row=1, col=1)

#  Propriétés axis btc € row=2, col=1
    fig.update_xaxes(title_text="Last update", row=2, col=1)
    fig.update_yaxes(title_text="euro", row=2, col=1)
    
# Propriétés axis btc $ row=3, col=1
    fig.update_xaxes(title_text="Last update", row=3, col=1)
    fig.update_yaxes(title_text="dollar", row=3, col=1)

#  Propriétés axis eur market cap row=4, col=1
    fig.update_xaxes(title_text="Last update", row=4, col=1)
    fig.update_yaxes(title_text="eur_market_cap", row=4, col=1)

#  Propriétés axis eur 24h vol row=5, col=1
    fig.update_xaxes(title_text="Last update", row=5, col=1)
    fig.update_yaxes(title_text="eur_24h_vol", row=5, col=1)

# BANDE DE BOLLINGER
# Paramètres des bandes de Bollinger

    fenetre = 24  # Fenêtre de calcul de la moyenne mobile
    ecart_type_multiplicateur = 2  # Multiplicateur de l'écart type

# Calcul de la moyenne mobile simple  et de l'écart type

    df_btc_no_duplicated['MoyenneMobile'] = df_btc_no_duplicated["eur"].rolling(window=fenetre).mean()
    df_btc_no_duplicated['EcartType'] = df_btc_no_duplicated["eur"].rolling(window=fenetre).std()


# Calcul des bandes de Bollinger
    df_btc_no_duplicated['BollingerSup'] = df_btc_no_duplicated['MoyenneMobile'] + (df_btc_no_duplicated['EcartType'] * ecart_type_multiplicateur)
    df_btc_no_duplicated['BollingerInf'] = df_btc_no_duplicated['MoyenneMobile'] - (df_btc_no_duplicated['EcartType'] * ecart_type_multiplicateur)

# calcul de l'EMA
    df_btc_no_duplicated['EMA']  = df_btc_no_duplicated["eur"].ewm(span=fenetre, adjust=False).mean()

# RSI
# Période pour le calcul du RSI
    periode = 14
# Calcul des variations de prix (gains et pertes)
    df_btc_no_duplicated['Variation'] = df_btc_no_duplicated["eur"].diff()

# Séparer les gains et les pertes
    gains = df_btc_no_duplicated['Variation'].apply(lambda x: x if x > 0 else 0)
    pertes = df_btc_no_duplicated['Variation'].apply(lambda x: -x if x < 0 else 0)

# Calcul de la moyenne des gains et des pertes sur la période
    df_btc_no_duplicated['MoyenneGains'] = gains.rolling(window=periode).mean()
    df_btc_no_duplicated['MoyennePertes'] = pertes.rolling(window=periode).mean()

# Calcul du RSI
    df_btc_no_duplicated['RS'] = df_btc_no_duplicated['MoyenneGains'] / df_btc_no_duplicated['MoyennePertes']
    df_btc_no_duplicated['RSI'] = 100 - (100 / (1 + df_btc_no_duplicated['RS']))

# Dernière valeur = > RSI
    derniere_valeur_rsi = df_btc_no_duplicated['RSI'].iloc[-1].round(2)

# Graphique "cours et indicateurs BTC"

# SMA
    fig.append_trace(go.Scatter(
    x = df_btc_no_duplicated["last_update"],
    y=df_btc_no_duplicated['MoyenneMobile'],
    mode='lines',
    #line_color=' #abb2b9',
    name='Moyenne mobile simpe (SMA)'
    ),row=2, col=1)

# EMA
    fig.append_trace(go.Scatter(
    x = df_btc_no_duplicated["last_update"],
    y=df_btc_no_duplicated['EMA'],
    mode='lines',
    #line_color=' #abb2b9',
    name='Moyenne mobile exponentielle (EMA)'
    ),row=2, col=1)
    
 # BANDES DE BOLLINGER

# Bande SUP
    fig.append_trace(go.Scatter(
    x = df_btc_no_duplicated["last_update"],
    y=df_btc_no_duplicated['BollingerSup'],
    mode='lines',
    line_color=' #abb2b9',
    name='Bande de Bollinger supérieure'
    ),row=2, col=1)
# Bande INF
    fig.append_trace(go.Scatter(
    x = df_btc_no_duplicated["last_update"], 
    y=df_btc_no_duplicated['BollingerInf'], 
    mode='lines',
    line_color='#d5d8dc',
    fill= 'tonexty', 
    name='Bande de Bollinger inférieure'
    ),row=2, col=1)   
    
# RSI
    fig.append_trace(go.Scatter(
    x = df_btc_no_duplicated["last_update"],
    y=df_btc_no_duplicated['RSI'],
    mode='lines', name='RSI',
    line_color='#7FFFD4',
    ),row=1, col=1)
#RSI Zone de surachat > 70
    fig.add_hline(y=70, line_dash="dot", row=1, col=1, line_color='#FF0000', line_width=2)
#RSI Zone de survente < 30
    fig.add_hline(y=30, line_dash="dot", row=1, col=1, line_color='#FF0000', line_width=2)

# Cours BTC €
    fig.append_trace(go.Scatter(
    x = df_btc_no_duplicated["last_update"],
    y = df_btc_no_duplicated["eur"],
    name="cours BTC euro"
    ), row=1, col=1)
    
# Cours BTC $
    fig.append_trace(go.Scatter(
    x = df_btc_no_duplicated["last_update"],
    y = df_btc_no_duplicated["usd"],
    name="cours BTC dollar"
    ), row=2, col=1)

# Capitalisation boursière
    fig.append_trace(go.Scatter(
    x = df_btc_no_duplicated["last_update"],
    y = df_btc_no_duplicated["eur_market_cap"],
    name="capitalisation boursière"
    ), row=3, col=1)

# Volume de négociation sur 24h
    fig.append_trace(go.Scatter(
    x = df_btc_no_duplicated["last_update"],
    y = df_btc_no_duplicated["eur_24h_vol"],
    name="Volume de négociation sur 24 h"
    ), row=4, col=1)


    fig.add_annotation(text=f'Dernière valeur: {derniere_valeur_btc}',
                   x=df_btc_no_duplicated['last_update'].iloc[-1], y=derniere_valeur_btc,
                   showarrow=True, arrowhead=1, row=1, col=1)

    fig.add_annotation(text=f'Dernière valeur: {derniere_valeur_btc_usd}',
                   x=df_btc_no_duplicated['last_update'].iloc[-1], y=derniere_valeur_btc,
                   showarrow=True, arrowhead=1, row=2, col=1)
    
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(height=1200, width=1000, title_text="Evolution du cours du Bitcoin", hovermode = "x unified" )
    # fig.write_html("/GIT/Api/api_coingecko/btc_eur_usd_DEX_24h_dev.html") # Windows
    fig.write_html("/home/FBO/git/Api/api_coingecko/visu/btc_eur_usd_DEX_24h_dev.html")

# VISUALISATION ltc
@task
def visu_ltc(df_ltc_no_duplicated,derniere_valeur_ltc,derniere_valeur_ltc_usd):
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    
    fig = make_subplots(
        rows=4, cols=1,
        subplot_titles=("LTC euro last 24h", "LTC dollar last 24h","Capitalisation boursière last 24h","volume d'échange eur 24h"))

# Update xaxis properties
    fig.update_xaxes(title_text="Last update", row=1, col=1)
# Update yaxis properties
    fig.update_yaxes(title_text="euro", row=1, col=1)

# Update xaxis properties
    fig.update_xaxes(title_text="Last update", row=2, col=1)
# Update yaxis properties
    fig.update_yaxes(title_text="dollar", row=2, col=1)

# Update xaxis properties
    fig.update_xaxes(title_text="Last update", row=3, col=1)
# Update yaxis properties
    fig.update_yaxes(title_text="eur_market_cap", row=3, col=1)

# Update xaxis properties
    fig.update_xaxes(title_text="Last update", row=4, col=1)
# Update yaxis properties
    fig.update_yaxes(title_text="eur_24h_vol", row=4, col=1)

    fig.append_trace(go.Scatter(
    x = df_ltc_no_duplicated["last_update"],
    y = df_ltc_no_duplicated["eur"],
    name="cours LTC euro"
    ), row=1, col=1)

    fig.append_trace(go.Scatter(
    x = df_ltc_no_duplicated["last_update"],
    y = df_ltc_no_duplicated["usd"],
    name="cours LTC dollar"
    ), row=2, col=1)

    fig.append_trace(go.Scatter(
    x = df_ltc_no_duplicated["last_update"],
    y = df_ltc_no_duplicated["eur_market_cap"],
    name="capitalisation boursière"
    ), row=3, col=1)

    fig.append_trace(go.Scatter(
    x = df_ltc_no_duplicated["last_update"],
    y = df_ltc_no_duplicated["eur_24h_vol"],
    name="Volume de négociation sur 24 h"
    ), row=4, col=1)
    
    fig.add_annotation(text=f'Dernière valeur: {derniere_valeur_ltc}',
                   x=df_ltc_no_duplicated['last_update'].iloc[-1], y=derniere_valeur_ltc,
                   showarrow=True, arrowhead=1, row=1, col=1)

    fig.add_annotation(text=f'Dernière valeur: {derniere_valeur_ltc_usd}',
                   x=df_ltc_no_duplicated['last_update'].iloc[-1], y=derniere_valeur_ltc_usd,
                   showarrow=True, arrowhead=1, row=2, col=1)

    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(height=1200, width=1000, title_text="Evolution du cours du Litecoin", hovermode = "x unified" )
#fig.show()
    #fig.write_html("/GIT/Api/api_coingecko/visu/ltc_eur_usd_DEX_24h.html") # Windows
    fig.write_html("/home/FBO/git/Api/api_coingecko/visu/ltc_eur_usd_DEX_24h.html") # Linux

# VISUALISATION eth
@task
def visu_eth(df_eth_no_duplicated,derniere_valeur_eth,derniere_valeur_eth_usd): 
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    
    fig = make_subplots(
       rows=4, cols=1,
       subplot_titles=("ETH euro last 24h", "ETH dollar last 24h","Capitalisation boursière last 24h","volume d'échange eur 24h"))

# Update xaxis properties
    fig.update_xaxes(title_text="Last update", row=1, col=1)
# Update yaxis properties
    fig.update_yaxes(title_text="euro", row=1, col=1)

# Update xaxis properties
    fig.update_xaxes(title_text="Last update", row=2, col=1)
# Update yaxis properties
    fig.update_yaxes(title_text="dollar", row=2, col=1)

# Update xaxis properties
    fig.update_xaxes(title_text="Last update", row=3, col=1)
# Update yaxis properties
    fig.update_yaxes(title_text="eur_market_cap", row=3, col=1)

# Update xaxis properties
    fig.update_xaxes(title_text="Last update", row=4, col=1)
# Update yaxis properties
    fig.update_yaxes(title_text="eur_24h_vol", row=4, col=1)

    fig.append_trace(go.Scatter(
    x = df_eth_no_duplicated["last_update"],
    y = df_eth_no_duplicated["eur"],
    name="cours ETH euro"
    ), row=1, col=1)

    fig.append_trace(go.Scatter(
    x = df_eth_no_duplicated["last_update"],
    y = df_eth_no_duplicated["usd"],
    name="cours ETH dollar"
    ), row=2, col=1)

    fig.append_trace(go.Scatter(
    x = df_eth_no_duplicated["last_update"],
    y = df_eth_no_duplicated["eur_market_cap"],
    name="capitalisation boursière"
    ), row=3, col=1)

    fig.append_trace(go.Scatter(
    x = df_eth_no_duplicated["last_update"],
    y = df_eth_no_duplicated["eur_24h_vol"],
    name="Volume de négociation sur 24 h"
    ), row=4, col=1)
    
    fig.add_annotation(text=f'Dernière valeur: {derniere_valeur_eth}',
                   x=df_eth_no_duplicated['last_update'].iloc[-1], y=derniere_valeur_eth,
                   showarrow=True, arrowhead=1, row=1, col=1)

    fig.add_annotation(text=f'Dernière valeur: {derniere_valeur_eth_usd}',
                   x=df_eth_no_duplicated['last_update'].iloc[-1], y=derniere_valeur_eth_usd,
                   showarrow=True, arrowhead=1, row=2, col=1)

    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(height=1200, width=1000, title_text="Evolution du cours de l'Etherum", hovermode = "x unified" )
    # fig.write_html("/git/Api/api_coingecko/visu/eth_eur_usd_DEX_24h.html") # Windows
    fig.write_html("/home/FBO/git/Api/api_coingecko/visu/eth_eur_usd_DEX_24h.html") # Linux
    

@flow(name="BTC Info", log_prints=True)    
def btc_info():
    simple_price = request()
    eur, usd,eur_24h_vol, eur_market_cap, last_updated_at, ltc_eur, ltc_usd, ltc_eur_24h_vol, ltc_eur_market_cap, ltc_last_updated_at, eth_eur, eth_usd, eth_eur_24h_vol, eth_eur_market_cap, eth_last_updated_at = parse_api_coingecko(simple_price)
    last_update_1,ltc_last_updated,eth_last_updated =  transfo(last_updated_at,ltc_last_updated_at,eth_last_updated_at)
    insertion = insert(eur,usd,last_update_1,eur_market_cap,eur_24h_vol,ltc_eur,ltc_usd,ltc_eur_24h_vol,ltc_eur_market_cap,ltc_last_updated,eth_eur,eth_usd,eth_eur_24h_vol,eth_eur_market_cap,eth_last_updated)
    df_btc_no_duplicated,df_ltc_no_duplicated,df_eth_no_duplicated = dataframe()
    derniere_valeur_btc, derniere_valeur_btc_usd,derniere_valeur_ltc,derniere_valeur_ltc_usd,derniere_valeur_eth,derniere_valeur_eth_usd = last_value(df_btc_no_duplicated,df_ltc_no_duplicated,df_eth_no_duplicated)
    visu_1 = visu_btc(df_btc_no_duplicated,derniere_valeur_btc, derniere_valeur_btc_usd)
    visu_2 = visu_ltc(df_ltc_no_duplicated,derniere_valeur_ltc,derniere_valeur_ltc_usd)
    visu_3 = visu_eth(df_eth_no_duplicated,derniere_valeur_eth,derniere_valeur_eth_usd)
   
if __name__ == "__main__":
    # Call a flow function for a local flow run!
    btc_info()

btc_info.visualize()
    
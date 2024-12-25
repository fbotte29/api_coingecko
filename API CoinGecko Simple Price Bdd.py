#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import time
import requests
import sqlite3
import pandas as pd


# ##### Capitalisation boursière = Cours actuel x Offre en circulation
# 
# ##### Désigne la valeur marchande totale de l’offre en circulation d’une crypto-monnaie. Semblable à la mesure du marché boursier  qui multiplie le cours par action par les actions facilement disponibles sur le marché (non détenues ni bloquées par des  initiés, des gouvernements).

# In[ ]:


## REQUEST
#Obtenir le prix actuel de toutes les crypto-monnaies dans toutes les autres devises prises en charge dont vous avez besoin.
response_5 = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Clitecoin%2Cethereum&vs_currencies=eur%2Cusd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true&precision=2")
simple_price = response_5.json()
#print(simple_price)
#print(simple_price["bitcoin"]["eur_market_cap"])


# In[ ]:


## PARSE
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
    
#print('euro:',eur,"\n"'dollar:',usd,"\n"'capitalisation boursiere €:',eur_market_cap,"\n"'Volume de négociation sur 24 h:',eur_24h_vol,"\n"'derniere Maj Prix:',last_updated_at)

#print("\n")
#print('ltc_euro:',ltc_eur,"\n"'ltc_dollar:',ltc_usd,"\n"'capitalisation boursiere €:',ltc_eur_market_cap,"\n"'Volume de négociation sur 24 h:',ltc_eur_24h_vol,"\n"'derniere Maj Prix:',ltc_last_updated_at)
#print("\n")
#print('eth_euro:',eth_eur,"\n"'eth_dollar:',eth_usd,"\n"'capitalisation boursiere €:',eth_eur_market_cap,"\n"'Volume de négociation sur 24 h:',eth_eur_24h_vol,"\n"'derniere Maj Prix:',eth_last_updated_at)


# In[ ]:


## BDD
#création de la Bdd SQLite si existe + création de la connexion
conn = sqlite3.connect("ProjectBTC.db")
cur = conn.cursor()





# In[ ]:





# In[ ]:


## Transformation = TIME=> colonne last_update table btc

#last_updated_1 = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(last_updated_at))
last_updated_1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_updated_at))
#last_updated_1 = time.localtime(last_updated_at)
#formatted_local_time = time.strftime("%Y-%m-%d %H:%M:%S", last_updated_1) 
#print(last_updated_1)
#print(type(last_updated_1))


# In[ ]:


## Transformation = TIME  => colonne last_update table ltc

#last_updated_2 = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(last_updated_at))
ltc_last_update = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ltc_last_updated_at))

#print(ltc_last_update)
#print(type(ltc_last_update))


# In[ ]:


## Transformation = TIME  => colonne last_update table eth

#last_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(last_updated_at))
eth_last_update = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(eth_last_updated_at)) 

#print(eth_last_update)
#print(type(eth_last_update))


# In[ ]:


## INSERT => table btc
# Chemin vers la base de données sur Windows
db_path = 'E:\\projet\\api_coingecko\\projectBTC.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()
req1 = 'INSERT INTO btc(eur,usd,last_update,eur_market_cap,eur_24h_vol) VALUES(?,?,?,?,?)'
val1 = (eur,usd,last_updated_1,eur_market_cap,eur_24h_vol)
cur.execute(req1,val1)
conn.commit() 
cur.close()


# In[ ]:


## INSERT => table ltc
db_path = 'E:\\projet\\api_coingecko\\projectBTC.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()
req1 = 'INSERT INTO ltc(eur,usd,last_update,eur_market_cap,eur_24h_vol) VALUES(?,?,?,?,?)'
val1 = (ltc_eur,ltc_usd,ltc_last_update,ltc_eur_market_cap,ltc_eur_24h_vol)
cur.execute(req1,val1)
conn.commit() 
cur.close()


# In[ ]:


## INSERT => table eth
db_path = 'E:\\projet\\api_coingecko\\projectBTC.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()
req1 = 'INSERT INTO eth(eur,usd,last_update,eur_market_cap,eur_24h_vol) VALUES(?,?,?,?,?)'
val1 = (eth_eur,eth_usd,eth_last_update,eth_eur_market_cap,eth_eur_24h_vol)
cur.execute(req1,val1)
conn.commit() 
cur.close()


# In[ ]:


## UPDATE unixepoch line

#conn = sqlite3.connect("ProjectBTC.db")
#cur = connexion.cursor()
#req2 = 'update btc set last_update = datetime(last_update, 'unixepoch', 'localtime') where last_update like '16%';'

#cur.execute(req2)

#cur.close()


# In[ ]:


## PRINT => btc
#cur = conn.cursor()
# cur.execute("select * from btc")
#cur.execute("select eur,usd,last_update,eur_market_cap,eur_24h_vol from btc order by last_update DESC limit(10)")
#cur.execute("select * from btc WHERE DATE(last_update) = DATE('now')")
#records = cur.fetchall()

#print(records[0])


# In[ ]:


## PRINT => ltc
#cur = conn.cursor()
# cur.execute("select * from ltc")
#cur.execute("select eur,usd,last_update,eur_market_cap,eur_24h_vol from ltc order by last_update DESC limit(10)")
#cur.execute("select * from ltc WHERE DATE(last_update) = DATE('now')")
#records = cur.fetchall()

#print(records[0])


# In[ ]:


## PRINT => eth
#cur = conn.cursor()
# cur.execute("select * from eth")
#cur.execute("select eur,usd,last_update,eur_market_cap,eur_24h_vol from eth order by last_update DESC limit(10)")
#cur.execute("select * from eth WHERE DATE(last_update) = DATE('now')")
#records = cur.fetchall()

#print(records[0])


# In[ ]:


#DATAFRAME => df_btc

df_btc = pd.read_sql('''select * from btc WHERE DATE(last_update) = DATE('now')''',conn,)
#df_btc = pd.read_sql('select eur,usd,last_update,eur_market_cap,eur_24h_vol from btc order by last_update',conn,)
#df_btc = pd.read_sql('''select eur,usd,last_update from btc where last_update like '2023-08-17%' ''',conn,)
#df_btc = pd.read_sql('select eur,usd,last_update from btc order by last_update DESC limit(10)',conn,)
#df_btc


# In[ ]:


#DATAFRAME => df_ltc

df_ltc = pd.read_sql('''select * from ltc WHERE DATE(last_update) = DATE('now')''',conn,)
#df_btc = pd.read_sql('select eur,usd,last_update,eur_market_cap,eur_24h_vol from btc order by last_update',conn,)
#df_btc = pd.read_sql('''select eur,usd,last_update from btc where last_update like '2023-08-17%' ''',conn,)
#df_btc = pd.read_sql('select eur,usd,last_update from btc order by last_update DESC limit(10)',conn,)
#df_ltc


# In[ ]:


#DATAFRAME => df_eth

df_eth = pd.read_sql('''select * from eth WHERE DATE(last_update) = DATE('now')''',conn,)
#df_btc = pd.read_sql('select eur,usd,last_update,eur_market_cap,eur_24h_vol from eth order by last_update',conn,)
#df_btc = pd.read_sql('''select eur,usd,last_update from eth where last_update like '2023-08-17%' ''',conn,)
#df_btc = pd.read_sql('select eur,usd,last_update from eth order by last_update DESC limit(10)',conn,)
#df_eth


# In[ ]:


# DETECTION DE DOUBLON SQL table btc
df_btc_doublon = pd.read_sql('''SELECT *, COUNT(*) AS nbr_doublon FROM btc where DATE(last_update) = DATE('now') GROUP BY last_update HAVING COUNT(*) > 1 ''',conn,)
#df_btc_doublon = pd.read_sql('''SELECT COUNT(*) AS nbr_doublon, eur,last_update,eur_market_cap FROM btc  where last_update like '2023-08-05%' GROUP BY last_update HAVING COUNT(*) > 1 ''',conn,)
#df_btc_doublon


# In[ ]:


# DETECTION DE DOUBLON SQL table ltc
df_ltc_doublon = pd.read_sql('''SELECT *, COUNT(*) AS nbr_doublon FROM ltc where DATE(last_update) = DATE('now') GROUP BY last_update HAVING COUNT(*) > 1 ''',conn,)
#df_btc_doublon = pd.read_sql('''SELECT COUNT(*) AS nbr_doublon, eur,last_update,eur_market_cap FROM ltc  where last_update like '2023-08-05%' GROUP BY last_update HAVING COUNT(*) > 1 ''',conn,)
#df_ltc_doublon


# In[ ]:


# DETECTION DE DOUBLON SQL table eth
df_eth_doublon = pd.read_sql('''SELECT *, COUNT(*) AS nbr_doublon FROM eth where DATE(last_update) = DATE('now') GROUP BY last_update HAVING COUNT(*) > 1 ''',conn,)
#df_btc_doublon = pd.read_sql('''SELECT COUNT(*) AS nbr_doublon, eur,last_update,eur_market_cap FROM eth  where last_update like '2023-08-05%' GROUP BY last_update HAVING COUNT(*) > 1 ''',conn,)
#df_eth_doublon


# In[ ]:


# NBRE DE DOUBLONS => df_btc
df_btc.duplicated(subset='last_update').sum()


# In[ ]:


# NBRE DE DOUBLONS => df_ltc
df_ltc.duplicated(subset='last_update').sum()


# In[ ]:


# NBRE DE DOUBLONS => df_eth
df_eth.duplicated(subset='last_update').sum()


# In[ ]:


# BOOLEEN TRUE = DOUBLON => df_btc
#df_btc.duplicated(subset='last_update')
df_btc.duplicated(subset='last_update').value_counts()


# In[ ]:


# BOOLEEN TRUE = DOUBLON => df_ltc
#df_ltc.duplicated(subset='last_update')
df_ltc.duplicated(subset='last_update').value_counts()


# In[ ]:


# BOOLEEN TRUE = DOUBLON => df_eth
#df_eth.duplicated(subset='last_update')
df_eth.duplicated(subset='last_update').value_counts()


# In[ ]:


# SUPPRESSION DE DOUBLON => df_btc => df_btc_no_duplicated
df_btc_no_duplicated = df_btc.drop_duplicates(subset='last_update')
#df_btc_no_duplicated


# In[ ]:


# SUPPRESSION DE DOUBLON => df_ltc => df_ltc_no_duplicated
df_ltc_no_duplicated = df_ltc.drop_duplicates(subset='last_update')
#df_ltc_no_duplicated


# In[ ]:


# SUPPRESSION DE DOUBLON => df_eth => df_eth_no_duplicated
df_eth_no_duplicated = df_eth.drop_duplicates(subset='last_update')
#df_eth_no_duplicated


# In[ ]:


# VERIF NBRE DE DOUBLONS => df_btc_no_duplicated
df_btc_no_duplicated.duplicated(subset='last_update').sum()


# In[ ]:


# VERIF NBRE DE DOUBLONS => df_ltc_no_duplicated
df_ltc_no_duplicated.duplicated(subset='last_update').sum()


# In[ ]:


# VERIF NBRE DE DOUBLONS => df_eth_no_duplicated
df_eth_no_duplicated.duplicated(subset='last_update').sum()


# In[ ]:


# BOOLEEN TRUE = DOUBLON => df_btc_no_duplicated
df_btc_no_duplicated.duplicated(subset='last_update').value_counts()


# In[ ]:


# BOOLEEN TRUE = DOUBLON => df_ltc_no_duplicated
df_ltc_no_duplicated.duplicated(subset='last_update').value_counts()


# In[ ]:


# BOOLEEN TRUE = DOUBLON => df_eth_no_duplicated
df_eth_no_duplicated.duplicated(subset='last_update').value_counts()


# In[ ]:


# SUPPRESSION COLONNE 
#df_btc_0 = df_btc.drop(['last_update'],axis=1)
#df_btc_0


# In[ ]:


## TRANSFORMATION DATAFRAME
#df_btc_1 = pd.to_datetime(df_btc['last_update'], format='ISO8601')
#df_btc_1


# In[ ]:


## TRANSFORMATION DATAFRAME
# Convert datetype to string

#df_btc_1 = df_btc['last_update'].astype(str)


# In[ ]:


## TRANSFORMATION DATAFRAME
# concatenation dataframe
#df_btc_01 = pd.concat([df_btc_0, df_btc_1],axis=1)
#df_btc_01


# In[ ]:


## VISUALISATION

#import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.cm as cm
#import plotly.graph_objects as go
#import plotly.express as px

#%matplotlib inline

#plt.figure(figsize=(15,6))

#x = df_btc["last_update"]
#y = df_btc["eur"]  
      
#plt.plot(x, 
 #        y,
 #        linewidth = 4)

#plt.title('Evolution du prix du Bitcoin en €')
#plt.xlabel('Date')
#plt.xticks(rotation = 45)
#plt.ylabel('Prix du Bitcoin (en euros et en dollar')


# In[ ]:


## VISUALISATION

#import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.cm as cm
#import plotly.graph_objects as go
#import plotly.express as px
#from plotly.subplots import make_subplots

#x = df_btc["last_update"]
#y = df_btc["eur"]  

#y1 = df_btc["usd"]

#fig1 = px.line(df_btc, x=x, y=y1)
#fig1.update_layout(legend_title_text = "Evolution du prix du Bitcoin en $")
#fig1.update_xaxes(title_text="Last Update")
#fig1.update_yaxes(title_text="btc dollar")

#fig.show()
#fig1.show()


# In[ ]:


# Dernière valeur = > btc

derniere_valeur_btc = df_btc_no_duplicated['eur'].iloc[-1]
derniere_valeur_btc_usd = df_btc_no_duplicated['usd'].iloc[-1]
#print(derniere_valeur_btc)
#print(derniere_valeur_btc_usd)


# In[ ]:


# Dernière valeur = > ltc

derniere_valeur_ltc = df_ltc_no_duplicated['eur'].iloc[-1]
derniere_valeur_ltc_usd = df_ltc_no_duplicated['usd'].iloc[-1]
#print(derniere_valeur_ltc)
#print(derniere_valeur_ltc_usd)


# In[ ]:


# Dernière valeur = > eth

derniere_valeur_eth = df_eth_no_duplicated['eur'].iloc[-1]
derniere_valeur_eth_usd = df_eth_no_duplicated['usd'].iloc[-1]
#print(derniere_valeur_eth)
#print(derniere_valeur_eth_usd)


# In[ ]:


from plotly.subplots import make_subplots
import plotly.graph_objects as go
#get_ipython().run_line_magic('matplotlib', 'inline')

fig = make_subplots(
    rows=5, cols=1,
    subplot_titles=("RSI","BTC euro last 24h", "BTC dollar last 24h","Capitalisation boursière last 24h","volume d'échange eur 24h"))

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

# calcul du taux de variation = difference entre [(valeur d'arrivée - valeur de départ) \ valeur de départ] *100
#print(df_btc_no_duplicated['Variation'])
#df_btc_no_duplicated['Variation_pct_change'] = df_btc_no_duplicated["eur"].pct_change()
#taux_var = (df_btc_no_duplicated['Variation_pct_change']*100)
#taux_var_ok = 4500 * taux_var
#print(taux_var_ok.round(2))

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

# Cours BTC €
fig.append_trace(go.Scatter(
x = df_btc_no_duplicated["last_update"],
y = df_btc_no_duplicated["eur"],
line_color='#FFD700',
name="cours BTC euro"
),row=2, col=1)

# Cours BTC $
fig.append_trace(go.Scatter(
x = df_btc_no_duplicated["last_update"],
y = df_btc_no_duplicated["usd"],
name="cours BTC dollar"
),row=3, col=1)

# Capitalisation boursière
fig.append_trace(go.Scatter(
x = df_btc_no_duplicated["last_update"],
y = df_btc_no_duplicated["eur_market_cap"],
name="capitalisation boursière"
), row=4, col=1)

# Volume de négociation sur 24h
fig.append_trace(go.Scatter(
x = df_btc_no_duplicated["last_update"],
y = df_btc_no_duplicated["eur_24h_vol"],
name="Volume de négociation sur 24 h"
), row=5, col=1)

# Ajout dernière valeur sur graphique
fig.add_annotation(text=f'Dernière valeur: {derniere_valeur_btc}',
                   x=df_btc_no_duplicated['last_update'].iloc[-1], y=derniere_valeur_btc,
                   showarrow=True, arrowhead=1, row=2, col=1)

fig.add_annotation(text=f'Dernière valeur: {derniere_valeur_btc_usd}',
                   x=df_btc_no_duplicated['last_update'].iloc[-1], y=derniere_valeur_btc_usd,
                   showarrow=True, arrowhead=1, row=3, col=1)

fig.add_annotation(text=f'Dernière valeur: {derniere_valeur_rsi}',
                   x=df_btc_no_duplicated['last_update'].iloc[-1], y=derniere_valeur_rsi,
                   showarrow=True, arrowhead=1, row=1, col=1)

#Zone de surachat > 70
fig.add_hline(y=70, line_dash="dot", row=1, col=1, line_color='#FF0000', line_width=2)
#Zone de survente < 30
fig.add_hline(y=30, line_dash="dot", row=1, col=1, line_color='#FF0000', line_width=2)

fig.update_traces(mode="markers+lines", hovertemplate=None)
fig.update_layout(height=1200, width=1000, title_text="Evolution du cours du Bitcoin", hovermode = "x unified",template='plotly_dark' )



#fig.show()
btc_path = 'E:\\projet\\api_coingecko\\visu\\btc_eur_usd_DEX_24h_dev.html'
fig.write_html(btc_path)


# In[ ]:


from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(
    rows=4, cols=1,
    subplot_titles=("LTC euro last 24h", "LTC dollar last 24h","Capitalisation boursière last 24h","volume d'échange eur 24h"))

# Update x axis properties
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
                   x=df_btc_no_duplicated['last_update'].iloc[-1], y=derniere_valeur_ltc,
                   showarrow=True, arrowhead=5, row=1, col=1)

fig.add_annotation(text=f'Dernière valeur: {derniere_valeur_ltc_usd}',
                   x=df_btc_no_duplicated['last_update'].iloc[-1], y=derniere_valeur_ltc_usd,
                   showarrow=True, arrowhead=8, row=2, col=1)

fig.update_traces(mode="markers+lines", hovertemplate=None)
fig.update_layout(height=1200, width=1000, title_text="Evolution du cours du Litecoin", hovermode = "x unified" )
#fig.show()
ltc_path = 'E:\\projet\\api_coingecko\\visu\\ltc_eur_usd_DEX_24h_dev.html'
fig.write_html(ltc_path)

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
fig.update_xaxes(title_text="Last update", row=2, col=1)
# Update yaxis properties
fig.update_yaxes(title_text="eur_market_cap", row=2, col=1)

# Update xaxis properties
fig.update_xaxes(title_text="Last update", row=2, col=1)
# Update yaxis properties
fig.update_yaxes(title_text="eur_24h_vol", row=2, col=1)

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
#fig.show()
eth_path = 'E:\\projet\\api_coingecko\\visu\\eth_eur_usd_DEX_24h_dev.html'
fig.write_html(eth_path)

# In[ ]:


## LE VOLUME D'ECHANGE est une métrique importante dans le suivi des marchés financiers pour plusieurs raisons:
### LIQUIDITE : Un volume d'échange élevé est généralement associé à une meilleure liquidité du marché. Plus le volume est élevé, plus il est facile d'acheter ou de vendre un actif sans causer de fluctuations de prix excessives.
### TENDANCE : Le volume d'échange peut fournir des informations sur la direction d'une tendance. Des volumes élevés pendant une hausse ou une baisse de prix peuvent indiquer la force de cette tendance.
### CONFIRMATION : Les analystes techniques utilisent souvent le volume d'échange pour confirmer ou invalider les signaux de trading. Par exemple, une hausse des prix avec un volume élevé peut indiquer une tendance haussière plus solide.
### VOLATILITE : Les périodes de faible volume d'échange peuvent contribuer à une plus grande volatilité des prix, car il peut être plus facile pour un petit nombre de transactions d'influencer les prix.
### EVALUATION DU MARCHE: Le volume d'échange peut également donner une idée de l'intérêt actuel des investisseurs pour un actif particulier. Un volume élevé peut indiquer un intérêt accru, tandis qu'un volume faible peut indiquer un manque d'intérêt ou de participation.


# In[ ]:





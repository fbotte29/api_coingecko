-- Créer la table btc
CREATE TABLE IF NOT EXISTS btc(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eur INTEGER NOT NULL,
    usd INTEGER NOT NULL,
    last_update INTEGER NOT NULL,
    eur_market_cap INTEGER NOT NULL,
    eur_24h_vol INTEGER NOT NULL);
-- Créer la table ltc
CREATE TABLE ltc(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eur INTEGER NOT NULL,
    usd INTEGER NOT NULL,
    last_update INTEGER NOT NULL,
    eur_market_cap INTEGER NOT NULL,
    eur_24h_vol INTEGER NOT NULL);
-- Créer la table eth
CREATE TABLE eth(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eur INTEGER NOT NULL,
    usd INTEGER NOT NULL,
    last_update INTEGER NOT NULL,
    eur_market_cap INTEGER NOT NULL,
    eur_24h_vol INTEGER NOT NULL);
-- Créer la table sol
CREATE TABLE sol(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eur INTEGER NOT NULL,
    usd INTEGER NOT NULL,
    last_update INTEGER NOT NULL,
    eur_market_cap INTEGER NOT NULL,
    eur_24h_vol INTEGER NOT NULL);
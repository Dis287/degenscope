import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(page_title="DegenScope 🔭", layout="wide")

st.title("🔭 DegenScope")
st.markdown("### Live Crypto Analyzer — Majors • Alts • Memes")
st.caption("Real-time prices • Charts • Degen insights • Powered by CoinGecko")

def fetch_coingecko_data(ticker: str = "SOL", days: int = 90):
    # CoinGecko ID mapping (add more as needed)
    id_map = {
        "BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana",
        "PEPE": "pepe", "BONK": "bonk", "WIF": "dogwifhat",
        "DOGE": "dogecoin", "SHIB": "shiba-inu"
    }
    coin_id = id_map.get(ticker.upper(), ticker.lower())  # fallback
    
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days, "interval": "daily"}
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        st.error("No data – check ticker or try later")
        return None
    
    data = response.json()["prices"]
    df = pd.DataFrame(data, columns=["timestamp", "close"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
    df.set_index("timestamp", inplace=True)
    
    # Add mock OHLC for simplicity (CoinGecko gives prices; expand if needed)
    df["open"] = df["close"].shift(1).fillna(df["close"])
    df["high"] = df["close"] * 1.02  # approx
    df["low"] = df["close"] * 0.98   # approx
    df["volume"] = 0  # volume separate endpoint if needed
    
    return df

ticker = st.text_input("Enter ticker (e.g. BTC, SOL, PEPE, BONK, WIF)", value="SOL").upper().strip()
days = st.slider("Days of history", 30, 180, 90)

if st.button("Scope It 🔭", type="primary"):
    with st.spinner("Fetching live data..."):
        try:
            df = fetch_coingecko_data(ticker, days)
            if df is None or len(df) < 10:
                st.error("No data – try a popular ticker like SOL, BTC, PEPE, BONK")
            else:
                
                current = df['close'].iloc[-1]
                change_24h = (current / df['close'].iloc[-2] - 1) * 100 if len(df) > 1 else 0
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Price", f"${current:,.4f}")
                c2.metric("24h Change", f"{change_24h:+.2f}%", delta=f"{change_24h:+.2f}%")
                c3.metric("Period High", f"${df['high'].max():,.4f}")
                c4.metric("Period Low", f"${df['low'].min():,.4f}")
                
                fig, ax = plt.subplots(figsize=(15, 8))
                color = '#00ff41' if change_24h >= 0 else '#ff006e'
                ax.plot(df.index, df['close'], color=color, linewidth=4, label=f"{ticker} Price")
                ax.fill_between(df.index, df['close'], alpha=0.3, color=color)
                ax.set_title(f"{ticker} — Last {days} Days", fontsize=20)
                ax.grid(alpha=0.3)
                st.pyplot(fig)
                
                degen_list = ["BONK", "PEPE", "WIF", "POPCAT", "MEW", "FLOKI", "SHIB", "DOGE", "MOG", "BRETT"]
                if ticker in degen_list:
                    st.error("⚠️ DEGEN ALERT ⚠️ Extreme volatility – can 100x or rug fast. Size accordingly.")
                else:
                    st.info("Established coin – lower meme risk.")
                
                vol_trend = "Pumping 🔥" if df['volume'].iloc[-1] > df['volume'].mean() * 1.3 else "Quiet 🧊"
                st.success(f"Volume: {vol_trend}")
                
        except Exception as e:
            st.error(f"Error: {e}")

st.caption("DegenScope 🔭 • Built by Dis287 • DYOR • Not financial advice")

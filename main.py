import streamlit as st
from polygon import RESTClient
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(page_title="DegenScope 🔭", layout="wide")

st.title("🔭 DegenScope")
st.markdown("### Live Crypto Analyzer — Majors • Alts • Memes")
st.caption("Real-time prices • Charts • Degen insights • Powered by Polygon")

client = RESTClient()

ticker = st.text_input("Enter ticker (e.g. BTC, SOL, PEPE, BONK, WIF)", value="SOL").upper().strip()
days = st.slider("Days of history", 30, 180, 90)

if st.button("Scope It 🔭", type="primary"):
    with st.spinner("Fetching live data..."):
        poly_ticker = f"X:{ticker}USD"
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days + 50)
        
        try:
            aggs = client.get_aggs(poly_ticker, 1, 'day', from_date.date(), to_date.date())
            if not aggs or len(aggs) < 10:
                st.error("No data – try a popular ticker like SOL, BTC, PEPE, BONK")
            else:
                df = pd.DataFrame(aggs)
                df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
                df.set_index('date', inplace=True)
                df = df[['open', 'high', 'low', 'close', 'volume']].tail(days)
                
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

import ccxt, pandas_ta as ta, pandas as pd
import time, requests, warnings
warnings.filterwarnings('ignore')

TOKEN = "8643994439:AAEambPaQLiIq9YkiqmA0XDodr_iwEVRCT8"
CHAT_ID = "5449514702"

def send_tele(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.get(url, params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

def run_bot():
    ex = ccxt.mexc()
    print("🚀 Dang quet Future H1...")
    try:
        markets = ex.fetch_markets()
        future_symbols = [m['symbol'] for m in markets if m['linear'] or m['swap']]
        tickers = ex.fetch_tickers()
        symbols = [s for s in future_symbols if s in tickers and tickers[s].get('quoteVolume', 0) > 1000000]
        
        found = []
        for s in symbols[:300]:
            try:
                ohlcv = ex.fetch_ohlcv(s, timeframe='1h', limit=50)
                df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
                ma20 = ta.sma(df['c'], length=20).iloc[-1]
                gia = df['c'].iloc[-1]
                if gia > ma20 and (gia - ma20)/ma20 < 0.05:
                    found.append(f"📈 *{s.split(':')[0]}*\n💰 Gia: `{gia}`\n📏 MA20: `{round(ma20, 6)}` (+{round((gia-ma20)/ma20*100, 2)}%)")
                time.sleep(0.01)
            except: continue
        if found:
            send_tele("🛡️ *KEO LONG H1 TREN MA20:*\n\n" + "\n\n".join(found[:12]))
    except Exception as e: print(e)

if __name__ == "__main__":
    run_bot()
  

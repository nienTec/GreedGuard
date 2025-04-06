import yfinance as yf
import ta

def fetch_rsi(symbol: str, period: str = "6mo") -> float:
    """
    Fetches the latest RSI value for a given symbol.
    """
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period)

    if not hist.empty:
        hist["rsi"] = ta.momentum.RSIIndicator(hist["Close"], window=14).rsi()
        latest_rsi = hist["rsi"].iloc[-1]  # Most recent RSI value
        return round(latest_rsi, 2)
    else:
        return None

def fetch_rsi_for_all_indices():
    """
    Fetches the RSI values for all important indices.
    Returns a dictionary of {index_name: rsi_value}.
    """
    indices = {
        "S&P 500": "^GSPC",
        "DAX": "^GDAXI",
        "CSI 300": "000300.SS",
        "Nikkei 225": "^N225"
    }

    rsi_values = {}

    for name, symbol in indices.items():
        rsi = fetch_rsi(symbol)
        rsi_values[name] = rsi

    return rsi_values

if __name__ == "__main__":
    rsi_data = fetch_rsi_for_all_indices()
    print("RSI values of major indices:")
    for index, rsi in rsi_data.items():
        print(f"{index}: {rsi}")

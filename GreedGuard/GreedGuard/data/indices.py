import yfinance as yf

def fetch_index_changes():
    """
    Holt die Tagesveränderung der wichtigsten Indizes.
    """
    indices = {
        "S&P 500": "^GSPC",
        "DAX": "^GDAXI",
        "CSI 300": "000300.SS",
        "Nikkei 225": "^N225"
    }

    results = {}

    for name, symbol in indices.items():
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="360d")

        if len(hist) >= 1:

            year_close = hist["Close"].iloc[-360]
            month_close = hist["Close"].iloc[-30]
            week_close = hist["Close"].iloc[-7]
            yesterday_close = hist["Close"].iloc[-2]
            today_close = hist["Close"].iloc[-1]

            change_24h = ((today_close - yesterday_close) / yesterday_close) * 100
            change_week = ((today_close - week_close) / week_close) * 100
            change_month = ((today_close - month_close) / month_close) * 100
            change_year = ((today_close - year_close) / year_close) * 100

            average_120d = hist['Close'].iloc[-120:].mean()
            avaerage_diff = ((today_close - average_120d) / average_120d) * 100

            results[name] = {
                "value": round(today_close, 2),
                "value_change_24h":round(change_24h, 2),
                "value_change_week": round(change_week, 2),
                "value_change_month": round(change_month, 2),
                "value_change_year": round(change_year, 2),
                "value_average_120d": round(average_120d, 2),
                "value_average_diff": round(avaerage_diff, 2)
            }
        else:
            results[name] = {
                "value": None,
                "value_change_24h":None,
                "value_change_week": None,
                "value_change_month": None,
                "value_change_year": None,
                "value_average_120d": None,
                "value_average_diff": None
            }  # Keine Daten verfügbar

    return results

def print_index_changes():
    """
    Prints the index changes in a nice readable format.
    """
    print("\n=== Index Performance Overview ===")

    changes = fetch_index_changes()

    for index, data in changes.items():
        if data["value"] is not None:
            print(f"\n{index}:")
            print(f"  Current Value: {data['value']}")
            print(f"  Change 24h: {data['value_change_24h']}%")
            print(f"  Change 7 days: {data['value_change_week']}%")
            print(f"  Change 30 days: {data['value_change_month']}%")
            print(f"  Change 360 days: {data['value_change_year']}%")
            print(f"  Average 120 days: {data['value_average_120d']}")
            print(f"  Average Diff: {data['value_average_diff']}%")
        else:
            print(f"\n{index}: No data available.")


if __name__ == "__main__":

    print_index_changes()
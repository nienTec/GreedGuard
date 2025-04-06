from datetime import datetime

import yfinance as yf

from utils.database import insert_vix_data


#Request VIX data.
def fetch_vix(period: str):

    try:
        ticker = yf.Ticker("^VIX")
        return ticker.history(period=period)

    except Exception as e:
        print(f"Failed requesting VIX data: {e}")
        return None

#VIX values object
vix_hist_values = fetch_vix("30d")

#Current VIX value
def vix_value():


    if not vix_hist_values.empty:
        return round(vix_hist_values['Close'].iloc[-1], 2)
    else:
        return None

#VIX value change 24h
def vix_value_change_24h():

    if not vix_hist_values.empty:
        latest_close = vix_value()
        previous_close = round(vix_hist_values['Close'].iloc[-2], 2)

        change_percent = ((latest_close - previous_close) / previous_close) * 100

        return round(change_percent, 2)
    else:
        return None

def vix_value_change_week():

    if not vix_hist_values.empty:
        latest_close = vix_value()
        week_close = round(vix_hist_values['Close'].iloc[-7], 2)

        change_percent = ((latest_close - week_close) / week_close) * 100

        return round(change_percent, 2)
    else:
        return None

def vix_value_change_month():

    if not vix_hist_values.empty:
        latest_close = vix_value()
        month_close = round(vix_hist_values['Close'].iloc[-30], 2)

        change_percent = ((latest_close - month_close) / month_close) * 100

        return round(change_percent, 2)
    else:
        return None


if __name__ == "__main__":

    def vix_data():
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "value": vix_value(),
            "value_change": vix_value_change_24h()
        }

    vix_data = vix_data()

    print(vix_value())
    print(vix_value_change_24h(), "%")
    print(vix_value_change_week(), "%")
    print(vix_value_change_month(), "%")

    if vix_data:
        insert_vix_data(vix_data)
        print("VIX data saved into DB.")

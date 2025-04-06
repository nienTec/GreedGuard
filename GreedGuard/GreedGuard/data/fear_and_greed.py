import requests
import sqlite3
from utils.database import insert_fear_and_greed_data, init_db
from datetime import datetime

def fetch_fear_and_greed_index() -> dict:
    """
    Holt aktuelle Fear and Greed Index Werte von der API.
    """
    url = "https://fear-and-greed-index.p.rapidapi.com/v1/fgi"
    headers = {
        "X-RapidAPI-Key": "9e6190d7fcmsh66513aa84de7cebp1d7b36jsn00b622804a16",
        "X-RapidAPI-Host": "fear-and-greed-index.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Falls Fehler passiert
        data = response.json()

        result = {
            "current": data["fgi"]["now"]["value"],
            "one_week_ago": data["fgi"]["oneWeekAgo"]["value"],
            "one_month_ago": data["fgi"]["oneMonthAgo"]["value"],
            "one_year_ago": data["fgi"]["oneYearAgo"]["value"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return result

    except requests.RequestException as e:
        print(f"Failed to request fetch and fear data: {e}")
        return {}

def fetch_all_entries():
    """
    Holt alle Einträge aus der Fear and Greed Tabelle.
    """
    conn = sqlite3.connect("GreedGuard.db")  # Verbindung zur Datenbank
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fear_and_greed")  # Alle Daten auslesen
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":

    fear_and_greed_data = fetch_fear_and_greed_index

    init_db()

    if fear_and_greed_data:
        print("Fear and Greed Index values:")
        for key, value in fear_and_greed_data.items():
            print(f"{key}: {value}")

    if fear_and_greed_data:
        insert_fear_and_greed_data(fear_and_greed_data)
        print("Fear and greet data saved into DB.")

    entries = fetch_all_entries()
    for entry in entries:
        print(entry)
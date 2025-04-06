import sqlite3
from datetime import datetime

def init_db():
    """
    Erstellt die SQLite-Datenbank und die Tabelle, falls sie noch nicht existiert.
    """
    conn = sqlite3.connect("GreedGuard.db")
    cursor = conn.cursor()

    #Create fear and greet table.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fear_and_greed (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            value INTEGER
        )
    ''')

    # Create indices table.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS indices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            indice TEXT,
            value INTEGER
            value_change REAL
        )
    ''')

    # Create vix table.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vix (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            value REAL,
            value_change REAL
        )
    ''')

    # Create inflation table.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inflation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            value REAL            
        )
    ''')

    # Create unemployment table.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS unemployment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            value REAL
        )
    ''')

    # Create market analysis table.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS market_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            total_score INTEGER,
            fear_and_greed TEXT,
            indices TEXT
            vix TEXT
            inflation TEXT
            unemployment TEXT
        )
    ''')
    conn.commit()
    conn.close()

##############################################################################
############################ Insert Functions ################################
##############################################################################

#Insert fear and greed data into table.
def insert_fear_and_greed_data(data: dict):

    conn = sqlite3.connect("GreedGuard.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO fear_and_greed (date, value)
        VALUES (?, ?)
    ''', (
        data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        data.get("current")
    ))

    conn.commit()
    conn.close()

#Insert indices data into table.
def insert_indices_data(data: dict):

    conn = sqlite3.connect("GreedGuard.db")
    cursor = conn.cursor()

    cursor.execute('''
            INSERT INTO indices (date, indice, value, value_change)
            VALUES (?, ?, ?, ?)
        ''', (
        data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        data.get("indice"),
        data.get("value"),
        data.get("value_change")
    ))

    conn.commit()
    conn.close()

#Insert vix data into table.
def insert_vix_data(data: dict):

    init_db()

    conn = sqlite3.connect("GreedGuard.db")
    cursor = conn.cursor()

    cursor.execute('''
            INSERT INTO vix (date, value, value_change)
            VALUES (?, ?, ?)
        ''', (
        data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        data.get("value"),
        data.get("value_change")
    ))

    conn.commit()
    conn.close()

#Insert inflation into table.
def insert_inflation_data(data: dict):

    conn = sqlite3.connect("GreedGuard.db")
    cursor = conn.cursor()

    cursor.execute('''
            INSERT INTO inflation (date, value, value_change)
            VALUES (?, ?, ?)
        ''', (
        data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        data.get("value"),
        data.get("value_change")
    ))

    conn.commit()
    conn.close()

#Insert unemployment data into table.
def insert_unemployment_data(data: dict):

    conn = sqlite3.connect("GreedGuard.db")
    cursor = conn.cursor()

    cursor.execute('''
            INSERT INTO unemployment (date, value, value_change)
            VALUES (?, ?, ?)
        ''', (
        data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        data.get("value"),
        data.get("value_change")
    ))

    conn.commit()
    conn.close()

#Insert market analyze data into table.
def insert_market_analyze_data(data: dict):

    conn = sqlite3.connect("GreedGuard.db")
    cursor = conn.cursor()

    cursor.execute('''
                INSERT INTO market_analyze (date, total_score, fear_and_greed, indices, vix, inflation, unempleoyment)
                VALUES (?, ?, ?)
            ''', (
        data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        data.get("total_score"),
        data.get("fear_and_greed"),
        data.get("indices"),
        data.get("vix"),
        data.get("inflation"),
        data.get("unempleoyment")
    ))

    conn.commit()
    conn.close()
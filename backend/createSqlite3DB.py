import sys
import os
import sqlite3



def createDatabase(name='./db/stock.sqlite3'):
    con = sqlite3.connect(name)

    createTable = '''\
            CREATE TABLE IF NOT EXISTS STOCK
            (ID INTEGER PRIMARY KEY NOT NULL UNIQUE,
            code TEXT,
            name TEXT UNIQUE,
            select_start_date DATETIME NOT NULL,
            select_end_date DATETIME NOT NULL,
            industry TEXT,
            is_high_price_of_100days BOOLEAN NOT NULL );
            '''
    # DEFAULT (datetime('now', 'localtime'))
    cur = con.cursor()
    cur.execute(createTable)

if __name__ == "__main__":
    createDatabase('./db/stock.sqlite3')


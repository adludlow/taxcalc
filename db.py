import sqlite3
import os
import logging

def createTables(conn):
    conn.execute('''
    create table bank_account (
        id integer primary key autoincrement,
        name text,
        bank_name text
    )''')

    conn.execute('''
    create table bank_txn (
        id integer primary key autoincrement,
        date date, 
        amount real,
        txn_type text,
        description text,
        balance real,
        account_id integer,
        foreign key(account_id) references bank_account(id)
    )''')

def checkDB(conn):
    cur = conn.cursor()
    try:
        version = cur.execute('select * from version')
        return True
    except sqlite3.OperationalError as err:
        return False 

def initialiseDatabase(conn):
    createTables(conn)

    conn.commit()
    conn.close()
    
def connect(dbfile):
    logging.debug('connect')
    conn = sqlite3.connect(dbfile)
    if checkDB(conn):
        logging.debug('DB Exists.')
        pass
    else:
        logging.debug('Creatnig DB.')
        initialiseDatabase(conn)


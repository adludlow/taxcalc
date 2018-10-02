import sqlite3
import os
import logging
from dataTypes import Transaction, Account

def createTables(conn):
    conn.execute('''
    create table version (
        version text
    )''')

    conn.execute("insert into version(version) values('0.1')")

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
        print(version)
        return True
    except sqlite3.OperationalError as err:
        print(err)
        return False 

def initialiseDatabase(conn):
    createTables(conn)

    conn.commit()
    
def connect(dbfile):
    logging.debug('connect')
    conn = sqlite3.connect(dbfile)
    if checkDB(conn):
        logging.debug('DB Exists.')
        pass
    else:
        logging.debug('Creating DB.')
        initialiseDatabase(conn)

    return conn

def addAccount(conn, account):
    conn.execute('insert into bank_account(name, bank_name) values(:name, :bank_name)', {'name': account.name, 'bank_name': account.bank_name})

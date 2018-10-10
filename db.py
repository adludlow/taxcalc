import sqlite3
import os
import logging
import hashlib
import csv
from datetime import datetime
from dataTypes import Transaction, Account
from dbExceptions import AccountExistsException

datafiles = [
        'data/tax_code.csv',
        'data/txn_type.csv'
        ]

def createTables(conn):
    conn.execute('''
    create table version (
        version text
    )''')

    conn.execute("insert into version(version) values('0.1')")

    conn.execute('''
    create table tax_code (
        tax_code text primary key,
        name text,
        description text
    )''')

    conn.execute('''
    create table txn_type (
        id integer primary key autoincrement,
        name text,
        label text,
        accountant_code text,
        tax_code text,
        txn_direction text check(txn_direction = 'IN' or txn_direction = 'OUT'),
        foreign key(tax_code) references tax_code(tax_code)
    )''')

    conn.execute('''
    create table bank_account (
        id integer primary key autoincrement,
        name text,
        bank_name text,
        hash text,
        created_on date
    )''')

    conn.execute('''create unique index ba_hash_idx on bank_account(hash)''')

    conn.execute('''
    create table bank_txn (
        id integer primary key autoincrement,
        date date, 
        amount real,
        txn_type_id integer,
        description text,
        balance real,
        account_id integer,
        created_on date,
        foreign key(account_id) references bank_account(id),
        foreign key(txn_type_id) references txn_type(id)
    )''')

def loadData(conn, datafile):
    filename = os.path.basename(datafile)
    inserts = []
    with open(datafile, 'r') as f:
        if csv.Sniffer().has_header(f.read(1024)):
            f.seek(0)
            reader = csv.reader(f)
            header = next(reader)
            escapeTrans = str.maketrans({"'": r"\'"})

            for row in reader:
                if row != []:
                    params = ('?,' * len(row))[:-1]
                    insertStatement = f"insert into {filename[:-4]}({','.join(header)}) values({params})"
                    insertPair = (insertStatement, row)
                    inserts.append(insertPair)
        else:
            raise Exception(f"Attempted to load data file {datafile} with no header record.")

    for i in inserts:
        conn.execute(i[0], i[1])

def checkDB(conn):
    cur = conn.cursor()
    try:
        version = cur.execute('select * from version')
        return True
    except sqlite3.OperationalError as err:
        return False 

def initialiseDatabase(conn):
    createTables(conn)
    for f in datafiles:
        loadData(conn, f)

    conn.commit()
    
def connect(dbfile):
    logging.debug('connect')
    conn = sqlite3.connect(dbfile)
    if checkDB(conn):
        logging.debug('DB Exists.')
    else:
        logging.debug('Creating DB.')
        initialiseDatabase(conn)

    return conn

def addAccount(conn, account):
    try:
        h = hashlib.sha256()
        h.update(bytes(account.name + account.bank_name, encoding='utf-8'))
        cur = conn.cursor()
        cur.execute('insert into bank_account(name, bank_name, hash) values(:name, :bank_name, :hash)', {'name': account.name, 'bank_name': account.bank_name, 'hash': h.digest()})
        account.id = cur.lastrowid
        return account
    except sqlite3.IntegrityError as err:
        if str(err).startswith('UNIQUE constraint failed'):
            raise AccountExistsException('Account exists.')
        else:
            raise

def addBankTransaction(conn, txn):
    cur = conn.cursor()
    cur.execute('insert into bank_txn(date, amount, txn_type_id, description, balance, account_id) values(:date, :amount, :txn_type_id, :description, :balance, :account_id)',{
        'date': txn.date,
        'amount': txn.amount,
        'txn_type_id': txn.type,
        'description': txn.description,
        'balance': txn.balance,
        'account_id': txn.account.id
    })

    txn.id = cur.lastrowid
    return txn

def getAccountByName(conn, accountName):
    cur = conn.cursor()
    cur.execute('select * from bank_account where name = ?', (accountName,))
    result = cur.fetchone()
    return Account.fromDBRow(result)

def getAccounts(conn):
    cur = conn.cursor()
    cur.execute('select * from bank_account')
    accounts = cur.fetchall()
    for acc in accounts:
        print(acc)

def getAccountTransactions(conn, accountId):
    cur = conn.cursor()
    cur.execute('select date, amount, txn_type_id, description, balance from bank_txn where account_id = ?', (accountId,))
    rows = cur.fetchall()
    txns = []
    return [Transaction.fromDBRow(row) for row in rows]

    

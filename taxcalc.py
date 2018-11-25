import db
import csv
import logging
from dataTypes import Transaction, Account

DB_EXT = '.taxcalc.db'
BANK_TXN_FIELD_NAMES = ['date', 'amount', 'unk1', 'unk2', 'type', 'description', 'balance']

def getCompanyConnection(companyName):
    companyDBFile = companyName.replace(' ', '') + DB_EXT
    conn = db.connect(companyDBFile)
    return conn

def addCompanyAccount(companyConn, account):
    return db.addAccount(companyConn, account)

def processStatement(companyConn, account, statementLoc, preSave=lambda *args: None,  statementFormat='csv'):
    try:
        with open(statementLoc, 'r') as stmt:
            reader = csv.DictReader(stmt, BANK_TXN_FIELD_NAMES)
            for row in reader:
                txn = Transaction.fromCSVRow(row)
                txn.account = account
                txn = preSave(txn)
                db.addBankTransaction(companyConn, txn)
        return companyConn
    except Exception as err:
        raise

def getAccount(companyConn, accountName):
    return db.getAccountByName(companyConn, accountName)
    
def getAccountTransactions(companyConn, account):
    try:
        return db.getAccountTransactions(companyConn, account.id)
    except Exception as err:
        raise

def save(companyConn):
    try:
        companyConn.commit()
    except Exception as err:
        raise

def getTransactionTypes(companyConn):
    try:
        return db.getTransactionTypes(companyConn)
    except Exception as err:
        raise

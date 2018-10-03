import csv
import argparse
from datetime import datetime
import os
import logging
from dataTypes import Transaction, Account

def processStatementRow(row, account):
    return Transaction(
            date=datetime.strptime(row['date'], '%d %b %y'),
            amount=row['amount'],
            type=row['type'],
            description=row['description'],
            balance=row['balance'],
            account=account
            )

NABTxnFieldNames = ['date', 'amount', 'unk1', 'unk2', 'type', 'description', 'balance']

parser = argparse.ArgumentParser()
parser.add_argument('company', help='Company to open/create. This value is used when naming a new db.')
parser.add_argument('-l', '--loadstatement', dest='statement_loc', help='Loads a banks statement', required=True)
parser.add_argument('-a', '--addaccount', help='Prompts the user for the account details.')

parser.add_argument('--log', dest='loglevel')

args = parser.parse_args()

LOG_LEVEL = args.loglevel or 'WARNING'
os.environ['LOG_LEVEL'] = LOG_LEVEL
#logger = logging.getLogger(__name__)
logging.getLogger().setLevel(LOG_LEVEL)

import db

# Open or create DB.
companyDBFile = args.company + '.taxcalc.db'
conn = db.connect(companyDBFile)

account = Account(name='Cheque', bank_name='NAB');
account = db.addAccount(conn, account)
conn.commit()

with open(args.statement_loc) as csvfile:
    reader = csv.DictReader(csvfile, NABTxnFieldNames)
    for row in reader:
        txn = processStatementRow(row, account)
        db.addBankTransaction(conn, txn)
    conn.commit()

db.getAccounts(conn)
db.getTransactions(conn)


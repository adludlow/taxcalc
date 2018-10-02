import csv
import argparse
from datetime import datetime
import os
import logging
from dataTypes import Transaction, Account

def processStatementRow(row):
    return Transaction(
            date=datetime.strptime(row['date'], '%d %b %y'),
            amount=row['amount'],
            type=row['type'],
            description=row['description'],
            balance=row['balance']
            )

NABTxnFieldNames = ['date', 'amount', 'unk1', 'unk2', 'type', 'description', 'balance']

parser = argparse.ArgumentParser()
parser.add_argument('company', help='Company to open/create. This value is used when naming a new db.')
parser.add_argument('-l', '--loadstatement', dest='statement_loc', help='Loads a banks statement', required=True)
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
db.addAccount(conn, account)

with open(args.statement_loc) as csvfile:
    reader = csv.DictReader(csvfile, NABTxnFieldNames)
    txns = []
    for row in reader:
        txns.append(processStatementRow(row))



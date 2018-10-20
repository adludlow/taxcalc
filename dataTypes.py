from collections import namedtuple
from datetime import datetime

class Transaction:
    def __init__(
            self,
            id=None,
            date=None,
            amount=None,
            type=None,
            description=None,
            balance=None,
            account=None
            ):
        self.id=id
        self.date=date
        self.amount=amount
        self.type=type
        self.description=description
        self.balance=balance
        self.account=account

    @staticmethod
    def fromDBRow(row):
        return Transaction(
            date=datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'),
            amount=row[1],
            type=row[2],
            description=row[3],
            balance=row[4]
        )

    @staticmethod
    def fromCSVRow(row):
        return Transaction(
            date=datetime.strptime(row['date'], '%d %b %y'),
            amount=row['amount'],
            type=row['type'],
            description=row['description'],
            balance=row['balance']
        )

class Account:
    def __init__(
            self,
            id=None,
            name=None,
            bank_name=None,
            transactions=[]
            ):
        self.id=id
        self.name=name
        self.bank_name=bank_name
        self.transactions=transactions

    @staticmethod
    def fromDBRow(row):
        return Account(
            id = row[0],
            name = row[1],
            bank_name = row[2]
        )


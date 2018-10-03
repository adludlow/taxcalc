from collections import namedtuple

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


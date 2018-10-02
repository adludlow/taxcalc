from collections import namedtuple

Transaction = namedtuple('Transaction', ['date', 'amount', 'type', 'description', 'balance'])

Account = namedtuple('Account', ['name', 'bank_name'])

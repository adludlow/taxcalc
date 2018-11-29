import cmd2 as cmd
import taxcalc
from dataTypes import Transaction, Account
from tabulate import tabulate

class TransactionTypeSelector(cmd.Cmd):
    def __init__(self, txnTypes, txn):
        super(TransactionTypeSelector, self).__init__()
        self.txnTypes = txnTypes
        self.txn = txn
        self.txnTypeList = [f"{tt.id}: {tt.name}" for tt in self.txnTypes]
        self.txnTypeMap = {f"{t.id}": t for t in self.txnTypes}
        print(f"Select txn type for txn: {self.txn}")

    prompt = '(txn type) '

    def do_p(self, arg):
        print(self.txnTypeList)

    def do_exit(self, arg):
        return True

    def default(self, arg):
        if len(arg.argv) != 1 or len(arg.argv[0]) == 0:
            print('A Transaction Type id must be entered.')
            return

        typeId = arg.argv[0]
        print(typeId)
        if typeId in self.txnTypeMap:
            # Insert txn into db
            # Save match
            return True

        print(f"Transaction type {typeId} does not exist.")
        return True

class TaxCalcCli(cmd.Cmd):
    intro = 'Tax Calc - import bank statements and generate reports.'
    prompt = '(taxcalc) '

    companies = {}
    currentCompanyName = ''
    currentCompanyConn = None
    txnTypes = []
    txnTypeList = []
    txnTypeMap = {}

    def setCurrentCompany(self, companyName):
        self.currentCompanyName = companyName
        self.currentCompanyConn = self.companies[companyName]

    def do_save(self):
        currentCompanyConn.commit()

    def do_createCompany(self, arg):
        if len(arg.argv) < 2 or len(arg.argv[1]) == 0:
            print('Company Name can\'t be empty.')
            return

        companyName = arg.args

        'Create a new company and open it: createCompany "My Company"'
        conn = taxcalc.getCompanyConnection(companyName)
        self.companies[companyName] = conn
        self.setCurrentCompany(companyName)
        self.txnTypes = taxcalc.getTransactionTypes(self.currentCompanyConn)
        self.txnTypeList = [f"{int(tt.id)}: {tt.name}" for tt in self.txnTypes]
        self.txnTypeMap = {int(t.id): t for t in self.txnTypes}
        self.printableTxnTypeMap = {
                'id': [ int(t.id) for t in self.txnTypes ],
                'type': [ t.name for t in self.txnTypes ],
                'txn_direction': [ t.txn_direction for t in self.txnTypes ],
                'tax_code': [ t.tax_code for t in self.txnTypes ]
                }
        print(f"Company {companyName} created")

    def do_addAccount(self, arg):
        if len(arg.argv) != 3:
            print('addAccount takes 2 arguments, Account Name and Bank Name.')
            return

        name, bankName = arg.argv[1:]
        account = Account(name=name, bank_name=bankName)
        taxcalc.addCompanyAccount(self.currentCompanyConn, account)
        print(f"Account {name} added to company {self.currentCompanyName}")
    
    def printTxnTypeMap(self, txnTypeMap):
        print(tabulate(self.printableTxnTypeMap, headers='keys'));
        
    def preTxnSave(self, txn):
        loop = True
        while loop:
            print(f"Enter Transaction Type for transaction: {txn}")
            resp = input('(Txn Type) ')
            if resp == 'p':
                self.printTxnTypeMap(self.txnTypeMap)
            else:
                txnId = int(resp)
                txn.type = self.txnTypeMap[txnId]
                return txn

    def do_processStatement(self, arg):
        if len(arg.argv) != 3:
            print('processStatement takes 2 arguments, Account Name and Statement File.')
            return

        accountName, statementFile = arg.argv[1:]
        account = taxcalc.getAccount(self.currentCompanyConn, accountName)
        taxcalc.processStatement(self.currentCompanyConn, account, statementFile, preSave=self.preTxnSave)
        print(f"Statement {statementFile} loaded into account {accountName}")

    def do_getAccountTransactions(self, arg):
        if len(arg.argv) != 2:
            print('getAccountTransactions takes 1 argument: AccountName.')
            return

        account = taxcalc.getAccount(self.currentCompanyConn, arg.args)
        txns = taxcalc.getAccountTransactions(self.currentCompanyConn, account)
        
    def do_exit(self, arg):
        return True

if __name__ == '__main__':
    TaxCalcCli().cmdloop()

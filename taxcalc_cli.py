import cmd
import db
import csv
from dataTypes import Account, Transaction

BANK_TXN_FIELD_NAMES = ['date', 'amount', 'unk1', 'unk2', 'type', 'description', 'balance']

class TaxCalcCli(cmd.Cmd):
    intro = 'Tax Calc - import bank statements and generate reports.'
    prompt = '(taxcalc) '

    companies = {}
    currentCompanyConn = None

    def do_save(self):
        currentCompanyConn.commit()

    def do_createCompany(self, companyName):
        'Create a new company and open it: createCompany "My Company"'
        companyDBFile = companyName.replace(' ', '') + '.taxcalc.db'
        conn = db.connect(companyDBFile)
        self.companies[companyName] = conn
        self.currentCompanyConn = conn

    def do_addAccount(self, arg):
        name, bankName = arg.split()
        account = Account(name=name, bank_name=bankName)
        db.addAccount(self.currentCompanyConn, account)

    def do_processStatement(self, arg):
        accountName, statementFile = arg.split()
        try:
            account = db.getAccountByName(self.currentCompanyConn, accountName)
            with open(statementFile, 'r') as csvfile:
                reader = csv.DictReader(csvfile, BANK_TXN_FIELD_NAMES)
                for row in reader:
                    txn = processStatementRow(row)
                    txn.account = account
                    db.addBankTransaction(self.currentCompanyConn, txn)
        except Exception as err:
            print(err)
            raise

    def do_getAccountTransactions(self, accountName):
        try:
            account = db.getAccountByName(self.currentCompanyConn, accountName)
            txns = db.getAccountTransactions(self.currentCompanyConn, accountName)
        except Exception as err:
            print(err)
            raise

    def do_exit(self):
        return True

if __name__ == '__main__':
    TaxCalcCli().cmdloop()

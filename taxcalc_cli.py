import cmd
import taxcalc
from dataTypes import Transaction, Account

class TransactionType(cmd.Cmd):
    intro = 'Select Transaction Type:'
    prompt = '(txn type)'

    def default(self, line):
        print(f"{line} selected.")
        return True

class TaxCalcCli(cmd.Cmd):
    intro = 'Tax Calc - import bank statements and generate reports.'
    prompt = '(taxcalc) '

    companies = {}
    currentCompanyName = ''
    currentCompanyConn = None

    def setCurrentCompany(self, companyName):
        self.currentCompanyName = companyName
        self.currentCompanyConn = self.companies[companyName]

    def do_save(self):
        currentCompanyConn.commit()

    def do_createCompany(self, companyName):
        if len(companyName) == 0:
            print('Company Name can\'t be empty.')
            return

        'Create a new company and open it: createCompany "My Company"'
        conn = taxcalc.getCompanyConnection(companyName)
        self.companies[companyName] = conn
        self.setCurrentCompany(companyName)
        print(f"Company {companyName} created")

    def do_addAccount(self, arg):
        args = arg.split()
        if len(args) != 2:
            print('addAccount takes 2 arguments, Account Name and Bank Name.')
            return
        name, bankName = args
        account = Account(name=name, bank_name=bankName)
        taxcalc.addCompanyAccount(self.currentCompanyConn, account)
        print(f"Account {name} added to company {self.currentCompanyName}")
    
    def preTxnSave(self, txn):
        # Match txn type
        TransactionType().cmdloop()

        # Prompt if no match
        return None

    def do_processStatement(self, arg):
        accountName, statementFile = arg.split()
        account = taxcalc.getAccount(self.currentCompanyConn, accountName)
        taxcalc.processStatement(self.currentCompanyConn, account, statementFile, preSave=self.preTxnSave)
        print(f"Statement {statementFile} loaded into account {accountName}")

    def do_getAccountTransactions(self, accountName):
        account = taxcalc.getAccount(self.currentCompanyConn, accountName)
        txns = taxcalc.getAccountTransactions(self.currentCompanyConn, account)
        
    def do_exit(self, arg):
        return True

if __name__ == '__main__':
    TaxCalcCli().cmdloop()

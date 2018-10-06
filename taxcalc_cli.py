import cmd
import taxcalc
from dataTypes import Transaction, Account

class TaxCalcCli(cmd.Cmd):
    intro = 'Tax Calc - import bank statements and generate reports.'
    prompt = '(taxcalc) '

    companies = {}
    currentCompanyConn = None

    def do_save(self):
        currentCompanyConn.commit()

    def do_createCompany(self, companyName):
        'Create a new company and open it: createCompany "My Company"'

        conn = taxcalc.getCompanyConnection(companyName)
        self.companies[companyName] = conn
        self.currentCompanyConn = conn

    def do_addAccount(self, arg):
        name, bankName = arg.split()
        account = Account(name=name, bank_name=bankName)
        taxcalc.addCompanyAccount(self.currentCompanyConn, account)

    def do_processStatement(self, arg):
        accountName, statementFile = arg.split()
        account = taxCalc.getAccount(self.currentCompanyConn, accountName)
        taxCalc.processStatement(self.currentCompanyConn, account, staementFile)

    def do_getAccountTransactions(self, accountName):
        account = taxCalc.getAccount(self.currentCompanyConn, accountName)
        txns = taxCalc.getAccountTransactions(self.currentCompanyConn, account)
        
    def do_exit(self, arg):
        return True

if __name__ == '__main__':
    TaxCalcCli().cmdloop()

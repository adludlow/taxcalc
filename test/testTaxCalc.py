from unittest import TestCase
from dataTypes import Transaction, Account
import taxcalc

class TestTaxCalc(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.TEST_COMPANY = 'TEST_COMPANY'
        self.TEST_ACCOUNT_1 = 'Account1'
        self.TEST_BANK_TYPE = 'Bank1'
        self.TEST_STATEMENT_1_LOC ='test/test_data/test_statement_1.csv'

    def setUp(self):
        self.companyConn = taxcalc.getCompanyConnection(self.TEST_COMPANY)
        self.testAccount1 = Account(name = self.TEST_ACCOUNT_1, bank_name = self.TEST_BANK_TYPE)

    def test_addCompanyAccount(self):
        taxcalc.addCompanyAccount(self.companyConn, self.testAccount1)
        self.assertTrue(True)

    def test_processStatement(self):
        taxcalc.processStatement(self.companyConn, self.testAccount1, self.TEST_STATEMENT_1_LOC)
        self.assertTrue(True)

    def test_getAccountTransactions(self):
        txns = taxcalc.getAccountTransactions(self.companyConn, self.testAccount1)
        self.assertTrue(True)

from unittest import TestCase
from dataTypes import Transaction, Account
from os import remove
import logging
import taxcalc

logging.getLogger().setLevel('DEBUG')

TEST_COMPANY = 'TEST_COMPANY'
TEST_ACCOUNT_1 = 'Account1'
TEST_BANK_TYPE = 'Bank1'
TEST_STATEMENT_1_LOC ='test/test_data/test_statement_1.csv'

class TestTaxCalc(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_addEntities(self):
        companyConn = taxcalc.getCompanyConnection(TEST_COMPANY)

        testAccount1 = Account(name = TEST_ACCOUNT_1, bank_name = TEST_BANK_TYPE)
        testAccount1 = taxcalc.addCompanyAccount(
                companyConn, 
                testAccount1)

        self.assertTrue(testAccount1.id > 0)

        taxcalc.processStatement(
                companyConn,
                testAccount1,
                TEST_STATEMENT_1_LOC)

        txns = taxcalc.getAccountTransactions(companyConn, testAccount1)
        self.assertTrue(len(txns) == 54)

        account = taxcalc.getAccount(companyConn, testAccount1.name)

    def tearDown(self):
        remove(TEST_COMPANY + taxcalc.DB_EXT)

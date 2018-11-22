import sys
from taxcalc_cli import TaxCalcCli
from unittest import TestCase
from unittest.mock import create_autospec

TEST_COMPANY = "Vandalay Industries"
TEST_ACCOUNT_1 = "Cheque"
TEST_BANK_1 = "NAB"
TEST_STATEMENT_1 = "test/test_data/test_statement_1.csv"

class TestCli(TestCase):

    def setUp(self):
        self.mock_stdin = create_autospec(sys.stdin)
        self.mock_stdout = create_autospec(sys.stdout)

    def test_createCompany(self):
        """Testing `createCompany` command."""
        cli = TaxCalcCli(stdin=self.mock_stdin, stdout = self.mock_stdout)
        cli.onecmd(f"createCompany {TEST_COMPANY}")
        self.assertEqual(cli.currentCompanyName, TEST_COMPANY)

        result = cli.onecmd(f"addAccount {TEST_ACCOUNT_1} {TEST_BANK_1}")

        txnTypeCli = cli.onecmd(f"processStatement {TEST_ACCOUNT_1} {TEST_STATEMENT_1}")


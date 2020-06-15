import unittest
from pyless.tests.functional.test_utils import *
from pyless.utils.enums.parameter_keys import ParameterKeys as p
from pyless.database.models import create_tables
from pprint import pprint


class TestCreateLoan(unittest.TestCase):

    def test_create_loan(self):
        params = {
            p.MONTHLY_PAYMENT: 230,
            p.AMOUNT: 32100,
            p.LENGTH_OF_LOAN: 23,
            p.INTEREST_RATE: 1.0
        }

        pprint(params)

        sc = mock_pyless(params)
        create_tables(sc.db)
        sc.services.loans.create_item()

    def test_update_loan(self):
        params = {
            p.U_ID: 2,
            p.MONTHLY_PAYMENT: 111,
            p.LENGTH_OF_LOAN: 111,
            p.INTEREST_RATE: 1.1
        }
        sc = mock_pyless(params)
        create_tables(sc.db)
        sc.services.loans.update_item_by_id()

    def test_get_loan(self):
        params = {
            p.U_ID: '1'
        }
        sc = mock_pyless(params)
        pprint(sc.services.loans.get_item_by_id())

    def test_get_all_loans(self):
        sc = mock_pyless()
        pprint(sc.services.loans.list_all_items())
        sc.db.close_connection()


if __name__ == '__main__':
    unittest.main()

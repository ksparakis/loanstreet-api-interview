from pyless.database.models import *
from ..dao import Dao


class LoansBaseDao(Dao):

    def __init__(self, db, model=Loan):
        Dao.__init__(self, db, model)

    def add(self, amount,  interest_rate,  length_of_loan,  monthly_payment):
        new_obj = Loan(amount=amount, interest_rate=interest_rate, length_of_loan=length_of_loan, monthly_payment=monthly_payment)

        new_obj.save()
        return new_obj.id

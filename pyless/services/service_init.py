from pyless.services.src.loan_service import LoanService


class ServiceInit:

    def __init__(self, pycore):
        self.loans = LoanService(pycore)


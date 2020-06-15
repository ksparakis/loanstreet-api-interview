from pyless.services.service import Service
from pyless.utils.enums.main import GuardConfigEnums as gc


class LoanService(Service):

    def __init__(self, pyless):
        Service.__init__(self, pyless, pyless.db.loans)

    def create_loan(self):
        return Service.create_item(self)

    def update_loan(self):
        return Service.update_item_by_id(self)

    def get_loan_by_id(self):
        return Service.update_item_by_id(self)

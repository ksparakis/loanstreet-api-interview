from pyless.main import PylessCore
from pyless.utils.enums.main import GuardConfigEnums as gc
from pyless.utils.exceptions.managed_exceptions import *
from pyless.services.src.loan_service import LoanService


GUARD_CONFIG = {
    gc.key.PARAMS: {
        gc.param.AMOUNT: {gc.option.PARAMETER_TYPE: gc.param_type.BODY,
                          gc.option.IS_REQUIRED: True,
                          gc.option.REGEX: gc.reg.DOUBLE},
        gc.param.INTEREST_RATE: {gc.option.PARAMETER_TYPE: gc.param_type.BODY,
                                 gc.option.IS_REQUIRED: True,
                                 gc.option.REGEX: gc.reg.DOUBLE},
        gc.param.LENGTH_OF_LOAN: {gc.option.PARAMETER_TYPE: gc.param_type.BODY,
                                  gc.option.IS_REQUIRED: True,
                                  gc.option.REGEX: gc.reg.INT},
        gc.param.MONTHLY_PAYMENT: {gc.option.PARAMETER_TYPE: gc.param_type.BODY,
                                   gc.option.IS_REQUIRED: True,
                                   gc.option.REGEX: gc.reg.DOUBLE},
    }}


def lambda_handler(event, context):

    res = None
    try:
        pc = PylessCore(GUARD_CONFIG, context=context, event=event)
        loan = LoanService(pc)
        res = loan.create_loan()
    except ManagedException as e:
        # This was an expected error and will return the proper response
        print("A managed exception occured")
        print(e)
        res = e.to_response()
    except Exception as e:
        print("A non expected error occured")
        print(e)
        # we need a method that takes unmanaged exception and returns a server error/sends us an email about this.
        res = PylessCore.fmt_server_error(e, context)
    finally:
        print(res)
        return res

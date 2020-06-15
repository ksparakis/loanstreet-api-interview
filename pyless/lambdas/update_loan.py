from pyless.main import PylessCore
from pyless.utils.enums.main import GuardConfigEnums as gc
from pyless.utils.exceptions.managed_exceptions import *

# Every lambda will have a guard config, it will allow us to manage the input and permissions
GUARD_CONFIG = {
    gc.key.PARAMS:{
        gc.param.U_ID: {gc.option.PARAMETER_TYPE: gc.param_type.BODY,
                        gc.option.IS_REQUIRED: True},
        gc.param.AMOUNT: {gc.option.PARAMETER_TYPE: gc.param_type.BODY,
                          gc.option.IS_REQUIRED: False},
        gc.param.INTEREST_RATE: {gc.option.PARAMETER_TYPE: gc.param_type.BODY,
                                 gc.option.IS_REQUIRED: False},
        gc.param.LENGTH_OF_LOAN: {gc.option.PARAMETER_TYPE: gc.param_type.BODY,
                                  gc.option.IS_REQUIRED: False},
        gc.param.MONTHLY_PAYMENT: {gc.option.PARAMETER_TYPE: gc.param_type.BODY,
                                   gc.option.IS_REQUIRED: False},
    },
    gc.key.MINIMUM_PARAMS: 2
}


def lambda_handler(event, context):
    res = None
    try:
        pc = PylessCore(GUARD_CONFIG, context=context, event=event)
        res = pc.services.loans.update_item_by_id()
    except ManagedException as e:
        # This was an expected error and will return the proper response
        res = e.to_response()
    except Exception as e:
        # we need a method that takes unmanaged exception and returns a server error/sends us an email about this.
        res = PylessCore.fmt_server_error(e, context)
    finally:
        return res

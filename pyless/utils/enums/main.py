from .status import *
from .guard_config_keys import *
from .methods import *
from .parameter_keys import *
from .parameter_options import *
from .parameter_type import *
from .regxs import *


# a single class to import to bring in all enums for Guard Config
class GuardConfigEnums:
    param = ParameterKeys
    key = GuardConfigKeys
    method = Methods
    param_type = ParameterType
    option = ParameterOptions
    status = Status
    reg = Regxs

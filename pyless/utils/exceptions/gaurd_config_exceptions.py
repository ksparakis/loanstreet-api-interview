class GuardConfigException(Exception):
    """ Base class to throw an error when something within the guard
    config is not formatter properly. These errors are here strictly for
    the developers and users should never experience one of these,
    if they do it will be routed as a server error aka general error"""
    def __init__(self, error_msg, status_code="400"):
        pass


class MissingParamType(GuardConfigException):
    """You set an parameter type is missng"""
    pass


class MissingDefaultValue(GuardConfigException):
    pass


class MissingPermissionGroup(GuardConfigException):
    """You set an parameter type is missng"""
    pass


class MissingVerifyJWT(GuardConfigException):
    """You set an parameter type is missng"""
    pass


class InvalidParamType(GuardConfigException):
    """You set an invalid parameter type in the gaurd config"""
    pass


class InvalidPermissionLevel(GuardConfigException):
    """This error occurs when you set an invalid permission in the guard config"""
    pass

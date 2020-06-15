from pyless.main import *


class ManagedException(Exception):
    """ Common base_daos class for all expected errors that should return a specified
    error status code and message. This makes converting errors in the code
     to error msgs that get returned via lambda/api gateway straight forward"""
    status_code = ""
    error_msg = ""

    def __init__(self, error_msg, status_code="400"):
        self.status_code = status_code
        self.error_msg = error_msg
        pass

    def to_response(self):
        return PylessCore.fmt_response(self.status_code, {"error": self.error_msg})


class EntityNotFound(ManagedException):
    """Error for when a user is not found in database"""
    def __init__(self,
                 error_msg="Entity Was Not Found",
                 status_code="401"):
        ManagedException.__init__(self, error_msg, status_code)


class FailedUserVerification(ManagedException):
    """Error for when user verification fails"""
    def __init__(self,
                 error_msg="User verification failed, invalid token",
                 status_code="401"):
        ManagedException.__init__(self, error_msg, status_code)


class InvalidUserPermissions(ManagedException):
    """Error for when user verification fails"""
    def __init__(self,
                 error_msg="User Is Not Authorized to Access This Resource",
                 status_code="403"):
        ManagedException.__init__(self, error_msg, status_code)


class InvalidHttpMethod(ManagedException):
    """Raise when the http method does not match whats expected"""
    def __init__(self,
                 error_msg="Invalid http method",
                 status_code="400"):
        ManagedException.__init__(self, error_msg, status_code)


class InvalidParameterCount(ManagedException):
    def __init__(self,
                 error_msg="Not Enough Parameters Passed in",
                 status_code="400"):
        ManagedException.__init__(self, error_msg, status_code)


class ParamInvalidMinLength(ManagedException):
    """Raise when the http method does not match whats expected"""
    def __init__(self,
                 error_msg="Parameter had invalid min length",
                 status_code="400"):
        ManagedException.__init__(self, error_msg, status_code)


class ParamInvalidMaxLength(ManagedException):
    def __init__(self,
                 error_msg="Parameter had invalid max length",
                 status_code="400"):
        ManagedException.__init__(self, error_msg, status_code)


class ParamInvalidRegex(ManagedException):
    def __init__(self,
                 error_msg="Parameter did not pass regex",
                 status_code="400"):
        ManagedException.__init__(self, error_msg, status_code)


class ParamRequired(ManagedException):
    def __init__(self,
                 error_msg="Parameter was missing",
                 status_code="400"):
        ManagedException.__init__(self, error_msg, status_code)
    pass

from pyless.utils.enums.main import GuardConfigEnums as gc
from .verified_parameter import VerifiedParameter
from pyless.utils.exceptions.managed_exceptions import *


class Guardian:
    """ The guardian to our codebase, he checks to verify
     verification are met to access a lambda and he also verifies
      that the inputted event has all expected parameters"""
    __guard_config = None
    __auth_token = None
    __permission_token = None
    __event = None

    __user = None  # The user object containing all information about the person executing the lambda
    __parameters = None  # A parameters dictionary containing verified parameters and their extracted data

    def __init__(self, guard_config, event):
        self.__parameters = dict()
        self.__guard_config = guard_config
        self.__event = event
        self.verify_parameters()
        self.verify_minimum_parameters()

    def verify_http_method(self):
        """
        [OPTIONAL ON GUARD CONFIG]
        Verify that that the http Method passed in is valid with what the guard config
        is expecting.
        """
        try:
            received_method = self.__event['httpMethod']
        except KeyError as e:
            # raise InvalidEvent? or do we just want to leave this flexible,
            # this occurs if we send in the wrong event during testing
            return False

        try:
            expected_method = self.__guard_config[gc.key.METHOD]
        except KeyError as e:
            # Not defined in guard config so skip
            return True

        if expected_method != received_method:
            raise InvalidHttpMethod("Was expecting {}, but received {}".format(expected_method, received_method))
        return True

    def verify_parameters(self):
        """
        [OPTIONAL ON GUARD CONFIG]
        Here we check the guard config for any expected parameters, and pass in
        all the expected  parameter and the event into VerifyParameter to error check
        the parameter and extract it.
        :return:
        """

        try:
            params = self.__guard_config[gc.key.PARAMS]
        except KeyError as e:
            # Not defined in guard config so skip
            return True

        for param in params.keys():
            self.__parameters[param] = VerifiedParameter(param, params[param],  self.__event)

    def verify_minimum_parameters(self):
        try:
            _min = self.__guard_config[gc.key.MINIMUM_PARAMS]
            if _min > len(self.__parameters):
                raise InvalidParameterCount(error_msg=f"Expected a minimum of {_min} parameters passed in")
            return True
        except KeyError:
            # Not defined in guard config so skip
            return True

    def get_user(self):
        return self.__user

    def get_params(self):
        return self.__parameters

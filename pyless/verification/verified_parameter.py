from pyless.utils.enums.main import GuardConfigEnums as gc
from pyless.utils.exceptions.gaurd_config_exceptions import *
from pyless.utils.exceptions.managed_exceptions import *
import re
import json


class VerifiedParameter:
    key = None
    val = None
    param_config = None
    is_required = None

    def __init__(self,  key, param_config, event, val=None):
        self.key = key
        self.val = val
        if param_config is not None:
            self.param_config = param_config
            self.check_param_requirement()

            # if default value exists use it, if not overwriteable, if overwriteable attempt to get other value.
            default_val, is_overwriteable = self.extract_default_val(event)
            if is_overwriteable:
                try:
                    self.val = self.__parse_param(event)
                except Exception as err:
                    if default_val is not None:
                        self.val = default_val
                    else:
                        raise err
            else:
                if default_val is None:
                    raise MissingDefaultValue
                else:
                    self.val = default_val

            self.verify_param_regex()
            self.verify_param_min_length()
            self.verify_param_max_length()

    def extract_default_val(self, event):
        default_value = None
        is_overwriteable = True

        # default value doesnt exist return none and true
        try:
            default_value = self.param_config[gc.option.DEFAULT_VALUE]
        except KeyError:
            return default_value, is_overwriteable

        try:
            # we have a default value check if its overwritable
            if default_value is not None:
                is_overwriteable = self.param_config[gc.option.IS_OVERWRITEABLE]
        except KeyError:
            # default overwriteable is set to true if not defined
            return default_value, is_overwriteable

        # return the default value and if its overwriteable
        return default_value, is_overwriteable

    def __parse_param(self, event):
        """ Check the param type then attempt to get it from the event """
        try:
            param_type = self.param_config[gc.option.PARAMETER_TYPE]
        except KeyError:
            raise MissingParamType

        # This is a required field in the parameter type and should trigger
        # a fatal error for developer to catch if its not in guard_config.
        if param_type == gc.param_type.PATH:
            return self.extract_path_param(event)
        elif param_type == gc.param_type.BODY:
            return self.extract_body_param(event)
        elif param_type == gc.param_type.QUERY:
            return self.extract_query_param(event)
        else:
            raise InvalidParamType

    def extract_body_param(self, event):
        try:
            return json.loads(event['body'])[self.key]
        except KeyError:
            if self.is_required:
                raise ParamRequired("Parameter Not Found in raw json Body")

    def extract_path_param(self, event):
        try:
            return json.loads(event['pathParameters'])[self.key]
        except KeyError:
            if self.is_required:
                raise ParamRequired("Parameter Not Found in url path")

    def extract_query_param(self, event):
        try:
            return event['queryStringParameters'][self.key]
        except KeyError:
            if self.is_required:
                raise ParamRequired("Parameter Not Found in url query")

    def check_param_requirement(self):
        # if is required is not set in the guard_config then its default is false
        try:
            self.is_required = self.param_config[gc.option.IS_REQUIRED]
        except KeyError:
            self.is_required = False

    def verify_param_min_length(self):
        try:
            min_length = self.param_config[gc.option.MIN_LENGTH]
        except KeyError:
            # does not have a min length argument so skip
            return True

        if min_length > len(self.val):
            raise ParamInvalidMinLength(
                "{} needs to have a char length greater than {}"
                .format(self.key, min_length - 1))

    def verify_param_max_length(self):
        try:
            max_length = self.param_config[gc.option.MIN_LENGTH]
        except KeyError:
            # does not have a min length argument so skip
            return True

        if max_length < len(self.val):
            raise ParamInvalidMinLength(
                "{} needs to have a char length less than {}"
                .format(self.key, max_length + 1))

    def verify_param_regex(self):
        try:
            regex = self.param_config[gc.option.REGEX]
            pattern = re.compile(regex)
            if pattern.match(str(self.val)):
                return True
            else:
                raise ParamInvalidRegex(
                    "{} needs to comply with the following regex pattern {}".format(self.val, regex)
                )
        except KeyError:
            # does not have a regex argument so skip
            return True

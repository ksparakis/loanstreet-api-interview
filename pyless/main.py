from pyless.database.db_init import DbInit
from pyless.services.service_init import ServiceInit
from .db_config import DB_CREDENTIALS
from .verification.guardian import Guardian
import json
import datetime


class PylessCore:
    env = None
    event = None
    aws = None
    db = None
    user = None
    parameters = None
    services = None

    def __init__(self, guard_config=None, context=None, env=None, event=None, init_db=True, is_db_local=False):
        # We get it from context for add user, where its not an API call, for api calls get it from the env variable
        self.env = self.get_env(context, env)
        self.event = event

        if guard_config is not None:
            k = Guardian(guard_config, self.event)
            self.user = k.get_user()
            self.parameters = k.get_params()

        # TODO: figure out error handling strategy for database,
        #  should we be contacted via email if fails? to tell us database is potentially down.
        if init_db is True:
            # Allows us to init db optionally, in case we have a lambda only needing aws access
            credentials = self.get_db_credentials(is_db_local)
            self.db = DbInit(credentials)

        self.services = ServiceInit(self)

    @staticmethod
    def get_env(context, env):
        """If environment is pa.ssed in use that else get environment from context"""
        if context is not None:
            env_out = PylessCore.get_env_from_context(context)
        elif env is None:
            env_out = "PROD"
        elif env.upper() == "PROD" or env.upper() == "DEV":
            env_out = env
        else:
            env_out = "PROD"
        print("Running in "+env_out+" environment")
        return env_out

    def get_db_credentials(self, is_db_local):
        """We currently store all out database secrets in the db_config.py file, do
        not push this file up to gitlab. we will pass this around manually for security purposes.
        this function for now, just checks the env, and using the secret name defined in the db_config.py
        returns that set of database credentials."""
        if self.env == "PROD":
            secret_name = "prod_db"
            # TODO: Decide if we want to use secret manager or just a config, keeping price and security in mind
            # json.loads(aws.get_secret(secret_name))
        elif is_db_local:
            secret_name = "local_db"
        else:
            secret_name = "dev_db"
        return DB_CREDENTIALS[secret_name]

    @staticmethod
    def get_env_from_context(context):
        # TODO:test that this still works and if we need to come up with a better method for this.
        # This function parses the function name which will at the end contains the env variable.
        try:
            return context.invoked_function_arn.split(":")[7]
        except Exception as e:
            print(context.invoked_function_arn)
            # if testing local on cloud 9 this will return dev
            try:
                if context.invoked_function_arn.split(":")[6] == "test":
                    print("Testing locally detected setting env = DEV")
                    return "DEV"
                else:
                    print("error parsing env variable from context, setting to PROD by default")
                    return "PROD"
            except Exception as e:
                print("error parsing env variable from context, setting to PROD by default")
                return "PROD"

    @staticmethod
    def fmt_response(status_code, json_body):
        def json_parser(o):
            """a custom json parser to handle converting datetime to json and potentially other unknown obj,"""
            if isinstance(o, datetime.datetime):
                return o.isoformat()

        return {
            "isBase64Encoded": False,
            'statusCode': status_code,
            'body': json.dumps(json_body, default=json_parser),
            'headers': {
                'Content-Type': 'application/json',
            },
        }

    @staticmethod
    def fmt_server_error(err, context):
        # TODO: send an email to us with details of error
        env = PylessCore.get_env_from_context(context)
        # SNS(env).send_sns(err)
        return PylessCore.fmt_response(500, {
            "error": "A server error occurred, the team has been notified and will work towards solving this issue."})




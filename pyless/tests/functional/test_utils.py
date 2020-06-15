from pyless.main import PylessCore
from pyless.verification.verified_parameter import VerifiedParameter
import random
import string


def mock_pyless(params_dict={}):
    mocked_params = {}
    for key, val in params_dict.items():
        mocked_params[key] = VerifiedParameter(key=key, val=val, event=None, param_config=None)

    #sc = PylessCore(env="DEV", init_db=True, is_db_local=True)
    sc = PylessCore(env="DEV", init_db=True)

    sc.parameters = mocked_params
    return sc


def generate_random_string(n):
    """Generate a random string of fixed length """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(n))

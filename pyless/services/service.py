from abc import ABC, abstractmethod
from pyless.utils.enums.parameter_keys import ParameterKeys as key
from pyless.utils.utils import get_all_vars_from_class
from pyless.utils.utils import rows_to_list_of_dicts


class Service(ABC):
    sonara = None
    dao = None

    def __init__(self, sonara, dao):
        self.sonara = sonara
        self.dao = dao

    # TODO: Do we make these decators of lambda_handler
    # TODO: rename pyless core
    # TODO: figure out how to make a generic update function. (change gaurd config?)
    # TODO: unit tests? how do we handle them? do we generate all possible unit tests?
    # TODO: generate ParameterKeys from model
    # TODO: proper way to deal with nums

    def delete_item_by_id(self):
        print(f"sonara.db.{self.dao}")
        dao = eval(f"sonara.db.{self.dao}")

        params = self.sonara.parameters
        u_id = params[key.U_ID].val

        self.dao.delete_by_id(u_id)
        return self.sonara.fmt_response(200, {"msg": f"Successfully deleted {self.dao.model.__name__}, id:{u_id}"})

    def update_item_by_id(self):
        params = self.sonara.parameters
        u_id = params[key.U_ID].val
        del params[key.U_ID]
        value_map = dict()
        print(params)
        for param in params.values():
            print(param)
            value_map[param.key] = param.val
        self.dao.update_by_id(u_id, value_map)
        return self.sonara.fmt_response(200, {"msg": f"Successfully updated {self.dao.model.__name__}, id:{u_id}"})

    def create_item(self):
        """
        This is a generic add function. Given the model wea re calling it from we get all possible inputs,
        generate the dao function as a string than use eval to turn that string into proper python code and execute it.
        """
        ip = self.sonara.parameters
        expected_params = get_all_vars_from_class(self.dao.model)
        output_param_str = "self.dao.add("
        count = 0
        for param in expected_params:
            try:
                v = ip[param]
                output_param_str += f"{param}=ip[key.{param.upper()}].val"
                count += 1
                if count != len(ip):
                    output_param_str += ", "
            except KeyError as e:
                print(e)
                pass

        output_param_str += ")"
        print(output_param_str)
        res = eval(output_param_str)
        print(f"Added item to {self.dao.model.__name__} at position {res}")
        return self.sonara.fmt_response(200, {"msg": f"Successfully added item to {self.dao.model.__name__}s at id {res}"})

    def list_all_items(self):
        return self.sonara.fmt_response(200, {f"{self.dao.model.__name__}s": self.dao.get_all()})

    def get_item_by_id(self):
        params = self.sonara.parameters
        u_id = params[key.U_ID].val

        item = self.dao.get_by_id(u_id)
        return self.sonara.fmt_response(200, {"msg": f"Successfully retrieved {self.dao.model.__name__}",
                                              f"{self.dao.model.__name__}": item})

from pyless.utils.utils import rows_to_list_of_dicts
from playhouse.shortcuts import model_to_dict

class Dao:
    """The main Dao class to build all the subclasses from. Here we can
    create classes that have logic that tends to get reused such as a get all"""
    __db = None
    model = None

    def __init__(self, db, model):
        # We instantiate db here just in case we have complex queries that peewee cant handle
        self.__db = db
        self.model = model

    def __str__(self):
        return str(type(self).__name__)

    def get_all(self, status="active"):
        query = self.model.select().dicts()
        return rows_to_list_of_dicts(query)

    def delete_by_id(self, u_id):
        """
        :param u_id: id to update
        :return: void
        No error thrown on u_id miss
        """
        self.model.delete_by_id(u_id)

    def delete_batch(self, where_condition):
        """
        :param where_condition:
            ie. (User.registration_expired == True)
        :return: void
        """
        q = self.model.delete().where(where_condition)
        q.execute()

    def get_by_id(self, u_id):
        """
        :param u_id: id to fetch
        :return: entity fetched from table
        Errors on u_id miss
        """

        return model_to_dict(self.model.get_by_id(u_id))

    def update_by_id(self, u_id, values_map):
        """
        :param u_id: id to update
        :param values_map: dictionary of values i.e: {status: "inactive"} to update
        :return: void
        No error thrown on u_id miss
        """
        self.model.set_by_id(u_id, values_map)

    def update_batch(self, update_dict, where_condition=None):
        """
        :param update_dict: Dictionary containing mapping (model field -> updated field value)
            ie. {User.active: False}
        :param where_condition:
            ie. (User.registration_expired == True)
        :return: void
        """
        q = self.model.update(update_dict)
        if where_condition:
            q = q.where(where_condition)
        q.execute()

    def select(self, where_condition=None, order_by_condition=None):
        """
        :param where_condition:
            ie. (User.registration_expired == True)
        :param order_by_condition: ordering condition
            ie. @db.collation('reverse')
                def collate_reverse(s1, s2):
                    return -cmp(s1, s2)
                (collate_reverse.collation(Book.title))
        :return: Peewee select result #TODO: Change to database independent result object
        """
        q = self.model.select()
        if where_condition:
            q = q.where(where_condition)
        if order_by_condition:
            q = q.order_by(order_by_condition)
        return q

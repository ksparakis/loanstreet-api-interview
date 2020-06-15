from datetime import datetime
from peewee import *

proxy = Proxy()

""" 
    +++++++++ READ THIS ++++++++++++
    For every new table make sure tp add it into the create, and run the dao_gen.py script to generate the daos.
    tables function below
"""


def create_tables(db):
    """function for creating our database model in a live postgres database, call it once."""
    db.get_connection().create_tables([Loan])


class BaseModel(Model):
    def __str__(self):
        return str(type(self).__name__)

    class Meta:
        database = proxy


class Loan(BaseModel):
    amount = IntegerField()
    interest_rate = DoubleField()
    length_of_loan = IntegerField()
    monthly_payment = DoubleField()

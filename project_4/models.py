import os

from peewee import *


db = PostgresqlDatabase(os.getenv('PJ4_DB','test'), user='serhatbolsu', autocommit=True, autorollback=True)


class Task(Model):
    employee = CharField(max_length=100)
    startdate = DateField(formats=["%m/%d/%Y"])
    duration = IntegerField()
    task = CharField()
    notes = TextField(default='')

    class Meta:
        database = db

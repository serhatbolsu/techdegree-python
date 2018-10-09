import os

from peewee import *

db = SqliteDatabase('tasks.db')


class Task(Model):
    employee = CharField(max_length=100)
    startdate = DateField()
    duration = IntegerField()
    task = CharField()
    notes = TextField()

    def __str__(self):
        return self.task

    class Meta:
        database = db

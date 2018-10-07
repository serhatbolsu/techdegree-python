import os
import re

import datetime

from collections import OrderedDict
from peewee import *
from models import db, Task


def clear_screen():
    os.system('clear')
    print()


def display_tasks(tasks):
    if len(tasks) == 0:
        print("There are no logs found to be shown!\n")
        return
    index = 0
    while 0 <= index < len(tasks):
        t = tasks[index]
        clear_screen()
        print(f"Task Date: {t.startdate.strftime('%m/%d/%Y')}")
        print(f"Employee Name: {t.employee}")
        print(f"Task Name: {t.task}")
        print(f"Task Duration: {str(t.duration)}")
        print(f"Task Notes: {t.notes}")
        print("")
        print(f"Result {str(index+1)} out of {str(len(tasks))} \n")
        if index == 0 and len(tasks) == 1:
            letter = input("Press 'E'dit 'D'elete 'Q'uit \n> ").upper().strip()
        elif index == 0:
            letter = input("Press 'N'ext 'E'dit 'D'elete 'Q'uit \n> ").upper().strip()
        elif index != len(tasks) - 1:
            letter = input("Press 'N'ext 'P'revious 'E'dit 'D'elete 'Q'uit \n> ").upper().strip()
        else:
            letter = input("Press 'P'revious 'E'dit 'D'elete 'Q'uit \n> ").upper().strip()

        if letter == 'Q':
            break
        elif letter == 'N':
            index += 1
        elif letter == 'P':
            index -= 1
        elif letter == 'E':
            edit_work(t)
        elif letter == 'D':
            delete_work(t)


def find_by_employee():
    """Find by Employee"""
    clear_screen()
    selection = input("Enter employee name to search for:\n>").strip()
    possible_matches = Task.select(
        Task.employee, fn.COUNT(Task.id).alias('count')).group_by(
        Task.employee).where(Task.employee.contains(selection))
    if int(possible_matches.count()) > 1:
        employees = {}
        for i, t in enumerate(possible_matches):
            employees[i] = {'id': t.id, 'name': t.employee, "count": t.count}
            print(f"{str(i)}) {t.employee.capitalize()} has {t.count} entries")
        while True:
            try:
                selection = input(f"Enter # to view all entries from {selection}:\n> ").strip()
                tasks = Task.select().where(Task.employee == employees[int(selection)]['name'])
                display_tasks(tasks)
                break
            except:
                input(f"Your selection {selection} is not valid, press enter to continue")
    else:
        while True:
            try:
                tasks = Task.select().where(
                    Task.employee == possible_matches[0].employee)
                display_tasks(tasks)
                break
            except IndexError:
                input("There are no logs found to be shown!, press enter to continue")
                break
            except:
                input(f"Your selection {selection} is not valid, press enter to continue")


def find_by_date():
    """Find by Date"""
    clear_screen()
    dates = {}
    while True:
        # print("Choose one of the dates with work logged on:\n")
        # for i,t in enumerate(Task.select(Task.startdate, fn.COUNT(Task.id).alias('count')
        #                                  ).group_by(Task.startdate)
        #                      .order_by(fn.COUNT(Task.id).desc())):
        #     dates[i] = {"date": t.startdate, 'count': t.count}
        #     print(f"{str(i)}) {t.startdate} has {t.count} entries")
        try:
            selection = input("Enter date for entries on that date (ex. MM/DD/YYYY): \n> ").strip()
            if not len(re.findall(r'\d{2}/\d{2}/\d{4}', selection)) == 1:
                raise ValueError
            parsed_date = datetime.datetime.strptime(selection, "%m/%d/%Y")
            tasks = Task.select().where(Task.startdate == parsed_date)
            display_tasks(tasks)
            break
        except:
            input(f"Your selection {selection} is not valid, press enter to try again")


def find_by_date_range():
    """Find by Given the date range"""
    clear_screen()
    while True:
        try:
            selection = input("Enter date range for finding entries in between "
                              "(ex. 01/01/2010-12/29/2018): \n>").strip()
            if not len(re.findall(r'\d{2}/\d{2}/\d{4}-\d{2}/\d{2}/\d{4}',
                                  selection)) == 1:
                raise ValueError
            parsed_date_low, parsed_date_high = selection.split("-")
            tasks = Task.select().where(
                Task.startdate.between(parsed_date_low, parsed_date_high))
            display_tasks(tasks)
            break
        except:
            print("Format of your selection should be MM/DD/YYYY-MM/DD/YYYY")
            input(f"Your selection {selection} is not valid, press enter to continue")


def find_by_time_spent():
    """Find by Time Spent"""
    time_spent = input("Enter a time for based on timespent: ").strip()
    tasks = Task.select().where(Task.duration>=time_spent)
    display_tasks(tasks)


def find_by_search_term():
    """Find by Term (task name or notes)"""
    term = input("Enter a term, it can be Notes/Task Name): ").strip()
    tasks = Task.select().where(Task.task.contains(term) | Task.notes.contains(term))
    display_tasks(tasks)


def edit_work(task):
    """Edit an entry."""
    selection = input("""Which part would you like to edit: \n
     [date/name/duration/notes]\n> """).lower().strip()
    if selection == 'date':
        new_date = input("Enter a new date (DD/MM/YYYY): ").strip()
        task.startdate = datetime.datetime.strptime(new_date, "%d/%m/%Y").date()
        task.save()
    elif selection == 'name':
        new_name = input("Enter a new task name: ").strip()
        task.task = new_name
        task.save()
    elif selection == 'duration':
        new_duration = int(input("Enter a new duration: ").strip())
        task.duration = new_duration
        task.save()
    elif selection == 'notes':
        new_notes = input("Enter you new note: ").strip()
        task.notes = new_notes
        task.save()


def log_work():
    """Log your work for an employee"""
    clear_screen()
    employee = input("Enter your name: ").lower().strip()
    task = input("Enter your task: ").strip()
    duration = int(input("Enter how many minutes your worked: ").lower().strip())
    startdate = datetime.datetime.now().strftime('%m/%d/%Y')
    # print("Enter you entry. Press ctrl+d when finished.")
    # notes = sys.stdin.read().strip()
    notes = input("Enter your additional notes: ").strip()
    Task.create(employee=employee, task=task, duration=duration,
                startdate=startdate, notes=notes if notes != '' else '')


def delete_work(task):
    """Delete an entry."""
    if input("Are you sure? [yN]  ").lower() == 'y':
        task.delete_instance()
        input("\nEnter deleted. Press a key to continue")


def view_work():
    """View previously logged work"""
    menu = OrderedDict([
        ('a', find_by_employee),
        ('b', find_by_date),
        ('c', find_by_time_spent),
        ('d', find_by_search_term),
        ('e', find_by_date_range)
    ])
    choice = None
    clear_screen()
    while choice != 'q':
        print("Choose your search method: ")
        for key, value in menu.items():
            print(f"{key}) {value.__doc__}")
        print("\nType 'q' to quit.\n")
        choice = input('> ').lower().strip()
        if choice == 'q':
            break
        if choice in menu:
            menu[choice]()


def main():
    clear_screen()
    print("Welcome to Work Log Tracker")
    choice = None
    menu = OrderedDict([
        ('a', log_work),
        ('b', view_work)
    ])
    while choice != 'q':
        for key, value in menu.items():
            print(f"{key}) {value.__doc__}")
        print("\nType 'q' to quit.\n")
        choice = input('> ').lower().strip()
        if choice in menu:
            menu[choice]()

    print("\nSee you next time")


if __name__ == '__main__':
    db.connect()
    db.create_tables([Task], safe=True)
    main()

import os
import re

from csv_operation import CsvOperation

csv = CsvOperation('work_log.csv')


def entry_menu(data_list):
    """Display results and edit/delete/quit options menu"""
    pointer = 0
    while data_list is not None and 0 <= pointer < len(data_list):
        os.system('clear')
        data = data_list[pointer].split(",")
        print("Date: {},".format(data[0]))
        print(f"Title: {data[1]},")
        print(f"Time Spent: {data[2]} minutes,")
        print(f"Notes: {data[3]}")
        print()
        print(f"Result {str(pointer+1)} of {str(len(data_list))}\n")
        if pointer == 0 and len(data_list) == 1:
            action = input(
                "Press 'E'dit 'D'elete 'R'eturn to search menu\n> ").upper().strip()
        elif pointer == 0:
            action = input(
                "Press 'N'ext 'E'dit 'D'elete 'R'eturn to search menu\n> ").upper().strip()
        elif pointer != len(data_list) - 1:
            action = input(
                "Press 'N'ext 'P'revious 'E'dit 'D'elete 'R'eturn to search menu\n> ")\
                .upper().strip()
        else:
            action = input(
                "Press 'P'revious 'E'dit 'D'elete 'R'eturn to search menu\n> ").upper().strip()
        if action == 'R':
            break
        elif action == 'N':
            pointer += 1
        elif action == 'P':
            pointer -= 1
        elif action == 'E':
            edit_entry(data_list[pointer])
            break
        elif action == 'D':
            delete_entry(data_list[pointer])
            break
        else:
            print(f"Your input '{action}' not correct")
            input("Press enter to try again")


def search_by_date():
    while True:
        try:
            os.system("clear")
            print("Enter the date")
            user_date = input("Please use DD/MM/YYYY: ").strip()
            result = csv.find_by_date(user_date)
        except:
            print(f"Your input '{user_date}' not correct")
            input("Press enter to try again")
        else:
            return result


def search_by_time_spent():
    while True:
        try:
            os.system("clear")
            print("Enter the time spent")
            user_input = input("As in minutes (ex. 30): ")
            result = csv.find_by_time_spent(int(user_input))
        except:
            print(f"Your input '{user_input}' not correct")
            input("Press enter to try again")
        else:
            return result


def search_by_text():
    while True:
        try:
            os.system("clear")
            print("Input keyword will be search upon title/notes")
            user_input = str(input("Please enter keyword: ").strip())
            result = csv.find_by_keyword(user_input)
        except:
            print(f"Your input '{user_input}' not correct")
            input("Press enter to try again")
        else:
            return list(result)


def search_by_pattern():
    while True:
        try:
            os.system("clear")
            print("")
            user_input = str(input("Please input regex pattern: ").strip())
            result = csv.find_by_regex_pattern(user_input)
        except:
            print(f"Your input '{user_input}' not correct")
            input("Press enter to try again")
        else:
            return list(result)


def search_by_range_dates():
    while True:
        try:
            os.system("clear")
            print("Enter the start and end date")
            user_date = input("Please use 'DD/MM/YYYY,DD/MM/YYYY': ").strip()
            if not len(re.findall(r'(\d{2})/(\d{2})/(\d{4})',
                                  user_date)) == 2:
                raise ValueError
            result = csv.find_by_date_range(user_date.split(',')[0],
                                            user_date.split(',')[1])
        except ValueError:
            print(f"Your input '{user_date}' not correct")
            input("Press enter to try again")
        else:
            return list(result)


def search_for_entry():
    """Search for entries menu, you have various search options"""
    while True:
        try:
            os.system("clear")
            print("""Do you want to search by:
a) Exact Date
b) Time Spent
c) Text
d) Regex Pattern
e) Range of Dates
f) Return to main menu\n""")
            search_method = str(input("Do you want to search by: \n> "))
            if search_method == 'a':
                entry_menu(search_by_date())
            elif search_method == 'b':
                entry_menu(search_by_time_spent())
            elif search_method == 'c':
                entry_menu(search_by_text())
            elif search_method == 'd':
                entry_menu(search_by_pattern())
            elif search_method == 'e':
                entry_menu(search_by_range_dates())
            elif search_method == 'f':
                break
            else:
                raise ValueError
        except Exception:
            print(f"Your input '{search_method}' not correct")
            input("Press enter to try again")


def edit_entry(entry):
    """Edit entry during displaying results"""
    csv.delete_row(entry)
    add_new_entry()


def delete_entry(entry):
    """Delete entry during displaying results"""
    csv.delete_row(entry)
    print("'{}' is deleted".format(entry))
    input("Press enter to go back")


def add_new_entry():
    """Create new entry"""
    entry = {}
    questions = {"name": "What is your task name? \n> ",
                 "time_spend": "How much time did you spend in minutes (ex. 30)? \n> ",
                 "notes": "Do you want to add notes (you can leave it empty)? \n> "
                 }

    for k, v in questions.items():
        while True:
            try:
                os.system("clear")
                field = str(input(v).strip())
                if k == 'time_spend' and (1 > int(field) or int(field) > 1000):
                    raise ValueError()
                else:
                    entry[k] = field
                break
            except ValueError:
                print(f"Your input '{field}' not correct")
                input("Press enter to try again")
    csv.output_to_csv(**entry)


def main_menu():
    """Main menu to select add/display/exit"""
    while True:
        os.system("clear")
        print("a) Add a new entry")
        print("b) Search Previous Entries")
        print("c) Exit and Terminate Program")
        try:
            selection = str(input("Please select an option: \n> "))
            if selection not in ["a", "b", "c"]:
                raise ValueError
            else:
                break
        except ValueError:
            print(f"Your selection is '{selection}' not valid. Try again\n")
            input("Press enter to try again")

    if selection == 'a':
        return "new"
    elif selection == 'b':
        return "search"
    else:
        return "exit"


def main():
    """Runs program indefinitely until user selects to terminate"""
    program = True
    while program:
        selection = main_menu()
        if selection == 'new':
            add_new_entry()
        elif selection == 'search':
            search_for_entry()
        else:
            break
    print("Thank you for playing")


if __name__ == '__main__':
    main()

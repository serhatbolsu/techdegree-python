import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from unit_3.csv_operation import CsvOperation

csv = CsvOperation('work_log.csv')

def entry_menu(data_list):
    pointer = 0
    while data_list is not None and pointer < len(data_list):
        os.system('clear')
        data = data_list[pointer].split(",")
        print("Date: {},".format(data[0]))
        print(f"Title: {data[1]},")
        print(f"Time Spent: {data[2]} minutes,")
        print(f"Notes: {data[3]}")
        print()
        print(f"Result {str(pointer+1)} or {str(len(data_list))}")
        action = str(input("[N]ext, [E]dit, [D]elete, [R]eturn to search menu \n>"))
        if action.upper() == 'N':
            pointer +=1
        elif action.upper() == 'E':
            edit_entry(data_list[pointer])
            break
        elif action.upper() == 'D':
            delete_entry(data_list[pointer])
            break
        elif action.upper() == 'R':
            break
        else:
            print(f"Your input '{action}' not correct")
            print("Press enter to try again")

a

def search_by_date():
    while True:
        try:
            os.system("clear")
            print("Enter the date")
            user_date = str(input("Please use DD/MM/YYYY: "))
            result = csv.find_by_date(user_date)
        except:
            print(f"Your input '{user_date}' not correct")
            print("Press enter to try again")
        else:
            return result

def search_by_time_spent():
    while True:
        try:
            os.system("clear")
            print("Enter the time spent")
            user_input = str(input("As in minutes (ex. 30): "))
            result = csv.find_by_time_spent(user_input)
        except:
            print(f"Your input '{user_input}' not correct")
            print("Press enter to try again")
        else:
            return result

def search_by_text():
    while True:
        try:
            os.system("clear")
            print("Input keyword will be search upon title/notes")
            user_input = str(input("Please enter keyword: "))
            result = csv.find_by_keyword(user_input)
        except:
            print(f"Your input '{user_input}' not correct")
            print("Press enter to try again")
        else:
            return list(result)

def search_by_pattern():
    while True:
        try:
            os.system("clear")
            print("")
            user_input = str(input("Please input regex pattern: "))
            result = csv.find_by_regex_pattern(user_input)
        except:
            print(f"Your input '{user_input}' not correct")
            print("Press enter to try again")
        else:
            return list(result)

#TODO: not implemented
def search_by_range_dates():
    while True:
        try:
            os.system("clear")
            print("Enter the date")
            user_date = str(input("Please use DD/MM/YYYY: "))
            result = csv.find_by_date(user_date)
        except:
            print(f"Your input '{user_date}' not correct")
            print("Press enter to try again")
        else:
            return list(result)

def search_for_entry():
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
            if   search_method == 'a': entry_menu(search_by_date())
            elif search_method == 'b': entry_menu(search_by_time_spent())
            elif search_method == 'c': entry_menu(search_by_text())
            elif search_method == 'd': entry_menu(search_by_pattern())
            elif search_method == 'e': entry_menu(search_by_range_dates())
            elif search_method == 'f': break
            else:
                raise ValueError
        except Exception:
            print(f"Your input '{search_method}' not correct")
            print("Press enter to try again")

def edit_entry(entry):
    csv.delete_row(entry)
    add_new_entry()

def delete_entry(entry):
    csv.delete_row(entry)
    print("'{}' is deleted".format(entry))
    input("Press enter to go back")

def add_new_entry():
    entry = {}
    questions= {"name" : "What is your task name? \n> ",
               "time_spend" : "How much time did you spend in minutes (ex. 30)? \n> ",
               "notes": "Do you want to add notes (you can leave it empty)? \n> "
    }

    for k, v in questions.items():
        while True:
            try:
                os.system("clear")
                field = str(input(v)).strip()
                if k == 'time_spend' and (1 > int(field) or int(field) > 1000):
                    raise ValueError()
                else:
                    entry[k] = field
                break
            except ValueError:
                print(f"Your input '{field}' not correct")
                print("Press enter to try again")
    csv.output_to_csv(**entry)

def main_menu():
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

    if selection == 'a': return "new"
    elif selection == 'b': return "search"
    else: return "exit"

def main():
    program = True
    while program:
        selection = main_menu()
        if selection == 'new': add_new_entry()
        elif selection == 'search' : search_for_entry()
        else: break
    print("Thank you for playing")


if __name__ == '__main__': main()
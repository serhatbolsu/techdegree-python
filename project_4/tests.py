from io import StringIO
import unittest
import unittest.mock as mock

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app import *


class BaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Called when the program starts if not called as an imported module."""
        db.connect(reuse_if_open=True)
        db.drop_tables([Task])
        db.create_tables([Task], safe=True)

    @classmethod
    def tearDownClass(cls):
        db.drop_tables([Task])
        db.close()


class MenuTests(BaseTests):
    def setUp(self):
        Task.create_table(safe=True)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_main_menu_print(self, mock_stdout):
        with mock.patch('builtins.input', side_effect=['q']):
            main()
            self.assertIn("a) Log your work for an employee", mock_stdout.getvalue())
            self.assertIn("b) View previously logged work", mock_stdout.getvalue())

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_view_work_selection(self, mock_stdout):
        with mock.patch('builtins.input', side_effect=['q']):
            view_work()
            self.assertIn("a) Find by Employee", mock_stdout.getvalue())
            self.assertIn("b) Find by Date", mock_stdout.getvalue())
            self.assertIn("c) Find by Time Spent", mock_stdout.getvalue())
            self.assertIn("d) Find by Term (task name or notes)", mock_stdout.getvalue())

    def test_display_options_no_result(self):
        task = Task.select().where(Task.employee == "not existing")
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            display_tasks(task)
            self.assertIn("There are no logs found to be shown", mock_stdout.getvalue())

    def test_display_options_single_result(self):
        Task.create(employee="test_cruid", task="Writing Test Cases",
                    startdate=datetime.datetime.strptime("01/01/1990", "%d/%m/%Y").date(),
                    duration=100, notes="I will handle this in no time")
        tasks = Task.select().where(Task.task == "Writing Test Cases")
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with mock.patch('builtins.input', side_effect=['q']) as mock_input:
                display_tasks(tasks)
            self.assertIn("Task Date: 01/01/1990", mock_stdout.getvalue())
            self.assertIn("Employee Name: test_cruid", mock_stdout.getvalue())
            self.assertIn("Task Name: Writing Test Cases", mock_stdout.getvalue())
            self.assertIn("Task Duration: 100", mock_stdout.getvalue())
            self.assertIn("Task Notes: I will handle this in no time", mock_stdout.getvalue())
            self.assertIn("Result 1 out of 1", mock_stdout.getvalue())
            self.assertIn("Press 'E'dit 'D'elete 'Q'uit", mock_input.call_args_list[0][0][0])

    def test_display_options_multi_result(self):
        Task.create(employee="test_cruid", task="Writing Test Cases",
                    startdate=datetime.datetime.now().date(),
                    duration=100, notes="I will handle this in no time")
        Task.create(employee="test_cruid2", task="Reading Test Cases",
                    startdate=datetime.datetime.now().date(),
                    duration=300, notes="Easy Peasy")
        Task.create(employee="test_cruid3", task="Speaking",
                    startdate=datetime.datetime.now().date(),
                    duration=500, notes="More")
        tasks = Task.select()
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with mock.patch('builtins.input', side_effect=['n', 'n', 'p', 'q']) as mock_input:
                display_tasks(tasks)
                self.assertIn("Task Name: Writing Test Cases", mock_stdout.getvalue())
                self.assertIn("Task Duration: 100", mock_stdout.getvalue())
                self.assertIn("Task Notes: I will handle this in no time", mock_stdout.getvalue())
                self.assertIn("Result 1 out of 3", mock_stdout.getvalue())
                self.assertIn("Result 2 out of 3", mock_stdout.getvalue())
                print(mock_input.call_args_list[0][0][0])
                self.assertIn("Press 'N'ext 'E'dit 'D'elete 'Q'uit ",
                              mock_input.call_args_list[0][0][0])
                self.assertIn("Press 'N'ext 'P'revious 'E'dit 'D'elete 'Q'uit ",
                              mock_input.call_args_list[1][0][0])
                self.assertIn("Press 'P'revious 'E'dit 'D'elete 'Q'uit ",
                              mock_input.call_args_list[2][0][0])

    def tearDown(self):
        Task.drop_table(safe=True)


class CRUDTests(BaseTests):
    def setUp(self):
        Task.create_table(safe=True)
        self.task1 = Task.create(employee="test_cruid", task="Writing Test Cases",
                                 startdate=datetime.datetime.now().date(),
                                 duration=100, notes="I will handle this in no time")
        self.task2 = Task.create(employee="test_cruid", task="Thinking",
                                 startdate=datetime.datetime.strptime("01/01/1990",
                                                                      "%d/%m/%Y").date(),
                                 duration=300, notes="I will handle this in no time")
        self.task3 = Task.create(employee="test_other_employee", task="Reading",
                                 startdate=datetime.datetime.now().date(),
                                 duration=50, notes="Very fun times")
        self.task4 = Task.create(employee="Ztest_other_employeeZ", task="Reading",
                                 startdate=datetime.datetime.now().date(),
                                 duration=50, notes="Very hard times")

    def test_create_entry(self):
        name = "Test_user2"
        task = "Writing Hard Test Cases"
        user_input = [name, task, "300", "This is the hardest part"]
        with mock.patch('builtins.input', side_effect=user_input):
            log_work()
            t = Task.select().where(Task.task == "Writing Hard Test Cases").get()
            assert t.employee == name.lower()  # even check lower
            assert t.task == task

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_find_by_employee_entry(self, mock_stdout):
        user_input = ["test_other_employee", "0"]  # select the user with most entries
        with mock.patch('builtins.input', side_effect=user_input):
            with mock.patch('app.display_tasks', side_effect=[""]):
                find_by_employee()
                self.assertIn("test_other_employee", mock_stdout.getvalue())
                self.assertIn("has 1 entries",
                              mock_stdout.getvalue())  # check the # of entries for that user

    def test_find_by_employee_entry_wrong_selection(self):
        user_input = ["100", "emter", "0", "q"]
        with mock.patch('builtins.input', side_effect=user_input):
            self.assertRaises(KeyError, find_by_employee())

    def test_find_by_date(self):
        user_input = "01/01/1990"
        with mock.patch('builtins.input', return_value=user_input):
            with mock.patch('app.display_tasks') as mock_display_tasks:
                find_by_date()
                assert mock_display_tasks.called
                args = mock_display_tasks.call_args_list[0][0]
                assert args[0].get().employee == 'test_cruid'
                assert args[0].get().task == "Thinking"
                assert len(args[0]) == 1

    def test_find_by_date_range(self):
        user_input = "01/01/1990-12/30/2018"
        with mock.patch('builtins.input', return_value=user_input):
            with mock.patch('app.display_tasks') as mock_display_tasks:
                find_by_date_range()
                assert mock_display_tasks.called
                args = mock_display_tasks.call_args_list[0][0]
                assert args[0].get().employee == 'test_cruid'
                assert args[0].get().task == "Writing Test Cases"
                assert args[0].count() == 4

    def test_by_time_spent(self):
        user_input = "299"
        with mock.patch('builtins.input', return_value=user_input):
            with mock.patch('app.display_tasks') as mock_display_tasks:
                find_by_time_spent()
                assert mock_display_tasks.called
                args = mock_display_tasks.call_args_list[0][0]
                assert args[0].get().employee == 'test_cruid'
                assert args[0].get().duration == 300
                assert len(args[0]) == 1

    def test_find_by_search_term(self):
        user_input = "fun"
        with mock.patch('builtins.input', return_value=user_input):
            with mock.patch('app.display_tasks') as mock_display_tasks:
                find_by_search_term()
                assert mock_display_tasks.called
                args = mock_display_tasks.call_args_list[0][0]
                assert args[0].get().employee == 'test_other_employee'
                assert args[0].get().duration == 50
                assert len(args[0]) == 1

    def test_edit_entry(self):
        employee = "test_edit"
        taskname = "Writing Test Cases"
        task = Task.create(employee=employee, task=taskname,
                           startdate=datetime.datetime.now().date(),
                           duration=300, notes="I will handle this in no time")
        user_input = ['date', "01/01/1990", 'name', "Easy Cases", 'duration', "100", 'notes', ""]
        with mock.patch('builtins.input', side_effect=user_input):
            edit_work(task)  # Edit Date
            t = Task.select().where(Task.employee == "test_edit").get()
            assert t.startdate.strftime("%d/%m/%Y") == user_input[1]

            edit_work(task)  # Edit Task name
            t = Task.select().where(Task.employee == employee).get()
            assert t.task == user_input[3]

            edit_work(task)  # Edit Duration
            t = Task.select().where(Task.task == "Easy Cases").get()
            assert t.duration == int(user_input[5])

            edit_work(task)  # Edit Notes can be empty
            t = Task.select().where(Task.task == "Easy Cases").get()
            assert t.notes == user_input[7]

    def test_delete_entry(self):
        employee = "test_delete"
        taskname = "Writing Test Cases"
        task = Task.create(employee=employee, task=taskname,
                           startdate=datetime.datetime.now().date(),
                           duration=300, notes="I will handle this in no time")
        with mock.patch('builtins.input', side_effect=['y', 'smt']):
            delete_work(task)
            self.assertRaises(Task.DoesNotExist)

    def tearDown(self):
        Task.drop_table(safe=True)


if __name__ == '__main__':
    unittest.main()

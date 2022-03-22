from .views import AbstractView
from .models import Operation
from abc import ABC, abstractmethod
import tkinter as tk


class AbstractController(ABC):
    @property
    @abstractmethod
    def operation(self) -> Operation:
        """Operation attribute. Should be None at init"""

    @property
    @abstractmethod
    def current_question(self) -> int:
        """current_question attribute. Should be 0 at init"""

    @property
    @abstractmethod
    def current_score(self) -> int:
        """current_score attribute. Should be 0 at init"""

    @property
    @abstractmethod
    def kwargs(self) -> dict:
        """kwargs attribute. Should be an empty dict at init"""

    @abstractmethod
    def __init__(self, view: AbstractView, operations: dict, max_questions: int):
        """
        :param view: a view object
        :param operations: a dict of Operation objects (constant var)
        :param max_questions: the number of maximum questions (constant var)
        """

    @abstractmethod
    def start(self):
        """Initializes the view with its main menu"""

    @abstractmethod
    def send_question(self, operation: Operation = None):
        """
        Send an operation question based on the operation object.
        """

    @abstractmethod
    def get_operation_kwargs(self) -> dict:
        """Retrieves operands, operator and result from an operation obj"""

    @abstractmethod
    def assess_answer(self, answer: int):
        """
        Compares the user answer and the result in kwargs, then sends the
        assessment result to the view.
        """

    @abstractmethod
    def back_to_main_menu(self):
        """
        Reinitializes score and test progression prior to main menu display.
        """


class TkControlExt(ABC):
    @abstractmethod
    def capture_user_input(self, entry: tk.Entry):
        """
        Captures and checks if the Tkinter Entry object is valid.
        Needs to be an integer.
        """


class ConsoleControlExt(ABC):
    @abstractmethod
    def check_main_menu_input(self, user_input: str):
        """
        Captures and checks the console main menu input
        """

    @abstractmethod
    def check_user_answer(self, answer: str):
        """
        Captures and checks the user answer. Needs to be an integer
        """

    @abstractmethod
    def check_question_navigation(self, user_input: str):
        """
        Captures and checks the input needed to navigate towards next question
        or coming back to main menu.
        """

    @abstractmethod
    def check_end_of_test_navigation(self, user_input: str):
        """
        Captures and checks the input needed to navigate towards the main menu
        or exit the program.
        """


class BaseController(AbstractController):
    operation = None
    current_question = 0
    current_score = 0
    kwargs = {}

    def __init__(self, view, operations, max_questions):
        self.view = view
        self.operations = operations
        self.max_questions = max_questions

    def start(self):
        self.view.init_setup(self)

    def send_question(self, operation=None):
        if operation:
            self.operation = operation
        if self.current_question >= self.max_questions:
            self.view.display_results_summary()
        else:
            self.kwargs = self.get_operation_kwargs()
            self.current_question += 1
            self.view.display_question()

    def get_operation_kwargs(self):
        kwargs = {"operator": self.operation.operator}
        operand_1, operand_2 = self.operation.get_operands()
        kwargs["operand 1"] = operand_1
        kwargs["operand 2"] = operand_2
        kwargs["result"] = self.operation.get_result(operand_1, operand_2)
        return kwargs

    def assess_answer(self, answer):
        if answer == self.kwargs["result"]:
            result = True
            self.current_score += 1
        else:
            result = False
        self.view.display_result(result, answer)

    def back_to_main_menu(self):
        self.current_question = 0
        self.current_score = 0
        self.view.display_main_menu()


class TkinterController(BaseController, TkControlExt):
    def capture_user_input(self, entry):
        user_input = entry.get()
        try:
            answer = int(user_input)
            self.assess_answer(answer)
        except ValueError:
            err_msg = "You must enter an integer"
            self.view.display_question(err_msg=err_msg)


class ConsoleController(BaseController, ConsoleControlExt):
    def check_main_menu_input(self, user_input):
        if user_input == "EXIT":
            quit()
        try:
            user_input = int(user_input)
        except ValueError:
            self.view.display_main_menu()
        if 0 < user_input < len(self.operations) + 1:
            key = list(self.operations.keys())[user_input - 1]
            operation = self.operations[key]
            self.send_question(operation)
        else:
            self.view.display_main_menu()

    def check_user_answer(self, user_input):
        if user_input == "EXIT":
            quit()
        try:
            user_input = int(user_input)
            self.assess_answer(user_input)
        except ValueError:
            self.view.display_question(err_msg="Integer needed")

    def check_question_navigation(self, user_input):
        if user_input == "EXIT":
            quit()
        self.send_question()

    def check_end_of_test_navigation(self, user_input: str):
        if user_input == "EXIT":
            quit()
        self.back_to_main_menu()

from .views import View
from .models import Operation
import tkinter as tk


class Controller:
    operation: Operation = None
    current_question: int = 0
    current_score: int = 0
    kwargs = dict

    def __init__(self, view: View, operations: dict, max_questions: int):
        self.view = view
        self.operations = operations
        self.max_questions = max_questions

    def start(self):
        """Initializes the view with its main menu"""
        self.view.init_setup(self)

    def send_question(self, operation: Operation = None):
        """
        Send an operation question based on the operation object.
        """
        if operation:
            self.operation = operation
        if self.current_question >= self.max_questions:
            self.view.display_results_summary()
        else:
            self.kwargs = self.get_operation_kwargs()
            self.current_question += 1
            self.view.display_question()

    def get_operation_kwargs(self) -> dict:
        """Retrieves operands, operator and result from an operation obj"""
        kwargs = {"operator": self.operation.operator}
        operand_1, operand_2 = self.operation.get_operands()
        kwargs["operand 1"] = operand_1
        kwargs["operand 2"] = operand_2
        kwargs["result"] = self.operation.get_result(operand_1, operand_2)
        return kwargs

    def assess_answer(self, user_entry: tk.Entry):
        """
        Checks if the user input is an integer and compares it to the result
        in kwargs, the sends the assessment result.
        """
        answer = None
        try:
            answer = int(user_entry.get())
        except ValueError:
            err_msg = "You must enter an integer"
            self.view.display_question(err_msg=err_msg)
        if answer is not None:
            if answer == self.kwargs["result"]:
                result_str = f"You answered {answer}. This is correct!"
                self.current_score += 1
            else:
                result_str = f"You answered {answer}. Wrong answer! " \
                             f"The correct answer was {self.kwargs['result']}"
            self.view.display_result(result_str)

    def back_to_main_menu(self):
        """
        Reinitializes score and test progression prior to main menu display
        """
        self.current_question = 0
        self.current_score = 0
        self.view.display_main_menu()

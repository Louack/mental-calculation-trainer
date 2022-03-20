import tkinter as tk
from abc import ABC, abstractmethod
from functools import partial
from random import randint
from typing import Tuple, Callable

BG_COLOR: str = "steelblue"
FONT: str = "Courrier"
FONT_COLOR: str = "white"
MAX_QUESTIONS: int = 10


class Operation(ABC):
    @property
    @abstractmethod
    def operator(self):
        """"""

    @abstractmethod
    def get_operands(self):
        """"""

    @abstractmethod
    def get_result(self, operand_1: int, operand_2: int):
        """"""


class Addition(Operation):
    operator: str = "+"

    def get_operands(self):
        return randint(1, 99), randint(1, 99)

    def get_result(self, operand_1: int, operand_2: int):
        return operand_1 + operand_2


class Multiplication(Operation):
    operator: str = "X"

    def get_operands(self):
        return randint(2, 9), randint(2, 9)

    def get_result(self, operand_1: int, operand_2: int):
        return operand_1 * operand_2


class TkView(ABC):
    @property
    @abstractmethod
    def controller(self):
        """"""

    @abstractmethod
    def init_setup(self, controller):
        """"""

    @abstractmethod
    def display_main_menu(self):
        """"""

    @abstractmethod
    def display_question(self, err_msg: str = None):
        """"""

    @abstractmethod
    def display_result(self, text_result: str):
        """"""

    @abstractmethod
    def display_results_summary(self):
        """"""


class ConcreteTkView(TkView):
    controller = None
    root: tk.Tk
    current_frame: tk.Frame = None

    def init_setup(self, controller):
        self.controller = controller
        self.root_setup()
        self.display_main_menu()
        self.root.mainloop()

    def display_main_menu(self):
        main_menu = self.replace_current_frame()

        title = tk.Label(
            main_menu,
            text="Welcome to Mental Math Trainer!",
            font=(FONT, 40),
            fg=FONT_COLOR,
            bg=BG_COLOR
        )
        title.pack(expand=True)

        choice_text = tk.Label(
            main_menu,
            text="Choose a test:",
            font=(FONT, 25),
            fg=FONT_COLOR,
            bg=BG_COLOR
        )
        choice_text.pack(expand=True)

        buttons_frame = tk.Frame(main_menu, bg=BG_COLOR)
        buttons_frame.pack(expand=True)

        for name, operation in self.controller.operations.items():
            self.implement_button(frame=buttons_frame,
                                  btn_text=name,
                                  command=partial(
                                      self.controller.send_question, operation
                                  ))

    def display_question(self, err_msg: str = None):
        question_frame = self.replace_current_frame()

        self.implement_progression_label(question_frame)

        question = f"{self.controller.kwargs['operand 1']} " \
                   f"{self.controller.kwargs['operator']} " \
                   f"{self.controller.kwargs['operand 2']} ?"
        question_label = tk.Label(
            question_frame,
            text=question,
            font=(FONT, 40),
            fg=FONT_COLOR,
            bg=BG_COLOR
        )
        question_label.pack(expand=True)

        entry = tk.Entry(
            question_frame,
            width=5,
            font=(FONT, 20),
            justify='center')
        entry.pack(expand=True)

        self.implement_button(frame=question_frame,
                              btn_text="Send",
                              command=partial(
                                  self.controller.assess_answer,
                                  entry))

        if err_msg:
            error_label = tk.Label(
                question_frame,
                text=err_msg,
                font=(FONT, 40),
                fg=FONT_COLOR,
                bg=BG_COLOR
            )
            error_label.pack(expand=True)

        self.implement_button(frame=question_frame,
                              btn_text="Main Menu",
                              command=self.controller.back_to_main_menu)

    def display_result(self, text_result):
        result_frame = self.replace_current_frame()
        self.implement_progression_label(result_frame)

        result_label = tk.Label(
            result_frame,
            text=text_result,
            font=(FONT, 20),
            fg=FONT_COLOR,
            bg=BG_COLOR
        )
        result_label.pack(expand=True)

        self.implement_button(frame=result_frame,
                              btn_text="Next",
                              command=self.controller.send_question)

        self.implement_button(frame=result_frame,
                              btn_text="Main Menu",
                              command=self.controller.back_to_main_menu)

    def display_results_summary(self):
        results_frame = self.replace_current_frame()
        results_text = f"Your score: {self.controller.current_score} / " \
                       f"{self.controller.current_question}"

        results_label = tk.Label(
            results_frame,
            text=results_text,
            font=(FONT, 20),
            fg=FONT_COLOR,
            bg=BG_COLOR
        )
        results_label.pack(expand=True)

        self.implement_button(frame=results_frame,
                              btn_text="Main Menu",
                              command=self.controller.back_to_main_menu)

    def root_setup(self):
        self.root = tk.Tk()
        self.root.title("Operation Trainer")
        self.root.geometry("1280x720")
        self.root.maxsize(1280, 720)
        self.root.minsize(480, 360)
        self.root.config(background=BG_COLOR)

    def replace_current_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.current_frame.pack(expand=True)
        return self.current_frame

    def implement_progression_label(self, frame: tk.Frame):
        progress_text = f"Progress: {self.controller.current_question} / " \
                        f"{MAX_QUESTIONS}"
        progress_label = tk.Label(
            frame,
            text=progress_text,
            font=(FONT, 40),
            fg=FONT_COLOR,
            bg=BG_COLOR
        )
        progress_label.pack(expand=True)

    @staticmethod
    def implement_button(frame: tk.Frame,
                         btn_text: str,
                         command: Callable = None):
        button = tk.Button(
            frame,
            text=btn_text,
            font=(FONT, 20),
            command=command
        )
        button.pack(expand=True)


class Controller:
    operation: Operation = None
    current_question: int = 0
    current_score: int = 0
    kwargs = dict

    def __init__(self, view: TkView, operations: dict):
        self.operations = operations
        self.view = view

    def start(self):
        self.view.init_setup(self)

    def send_question(self, operation: Operation = None):
        if operation:
            self.operation = operation
        if self.current_question >= MAX_QUESTIONS:
            self.view.display_results_summary()
        else:
            self.kwargs = self.get_operation_kwargs()
            self.current_question += 1
            self.view.display_question()

    def get_operation_kwargs(self) -> dict:
        kwargs = {"operator": self.operation.operator}
        operand_1, operand_2 = self.operation.get_operands()
        kwargs["operand 1"] = operand_1
        kwargs["operand 2"] = operand_2
        kwargs["result"] = self.operation.get_result(operand_1, operand_2)
        return kwargs

    def assess_answer(self, user_entry):
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
        self.current_question = 0
        self.current_score = 0
        self.view.display_main_menu()


if __name__ == "__main__":
    OPERATIONS = {
        "Addition": Addition(),
        "Multiplication": Multiplication()
    }

    app = Controller(ConcreteTkView(), OPERATIONS)
    app.start()



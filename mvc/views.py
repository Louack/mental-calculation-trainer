import tkinter as tk
from abc import ABC, abstractmethod
from functools import partial
from typing import Callable

BG_COLOR: str = "steelblue"
FONT: str = "Courrier"
FONT_COLOR: str = "white"


class AbstractView(ABC):
    """Abstract view to interact with the program"""
    @property
    @abstractmethod
    def controller(self):
        """Must be of type 'Controller'"""

    @abstractmethod
    def init_setup(self, controller):
        """initializes the view by the controller. Must display main menu"""

    @abstractmethod
    def display_main_menu(self):
        """a main menu with a choice of tests to run"""

    @abstractmethod
    def display_question(self, err_msg: str = None):
        """
        An operation displayed by a text and an entry to collect the answer.
        """

    @abstractmethod
    def display_result(self, result: bool, answer: int):
        """
        Displays the correct/wrong result as text.
        """

    @abstractmethod
    def display_results_summary(self):
        """
        Displays the final score
        """


class TkinterView(AbstractView):
    """View using tkinter interface. Needs a Tkinter Controller"""
    controller = None
    root: tk.Tk
    current_frame: tk.Frame = None

    def init_setup(self, controller):
        self.controller = controller
        self.root_setup()
        self.display_main_menu()
        self.root.mainloop()

    def root_setup(self):
        self.root = tk.Tk()
        self.root.title("Operation Trainer")
        self.root.geometry("1280x720")
        self.root.maxsize(1280, 720)
        self.root.minsize(480, 360)
        self.root.config(background=BG_COLOR)

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
                                  self.controller.capture_user_input,
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

    def display_result(self, result, answer):
        result_frame = self.replace_current_frame()
        self.implement_progression_label(result_frame)

        if result:
            text_result = f"You answered {answer}. This is correct!"
        else:
            text_result = f"You answered {answer}. Wrong answer! " \
                          f"The correct answer was " \
                          f"{self.controller.kwargs['result']}"

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

    def replace_current_frame(self):
        """
        Allows to switch between frames.
        """
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.current_frame.pack(expand=True)
        return self.current_frame

    def implement_progression_label(self, frame: tk.Frame):
        """Implements the test progression"""
        progress_text = f"Progress: {self.controller.current_question} / " \
                        f"{self.controller.max_questions}"
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
        """Implements buttons with a command"""
        button = tk.Button(
            frame,
            text=btn_text,
            font=(FONT, 20),
            command=command
        )
        button.pack(expand=True)


class ConsoleView(AbstractView):
    """View using console interface. Needs a Console Controller"""
    controller = None

    def init_setup(self, controller):
        self.controller = controller
        self.display_main_menu()

    def display_main_menu(self):
        print("Welcome to Mental Math Trainer")
        print("Enter the number associated with the test you want to perform "
              "or 'EXIT' to quit the program:")
        for i, name in enumerate(self.controller.operations, 1):
            print(f"{i} - {name}")
        user_input = input()
        self.controller.check_main_menu_input(user_input)

    def display_question(self, err_msg=None):
        print(f"Question {self.controller.current_question} / "
              f"{self.controller.max_questions}")
        print(f"{self.controller.kwargs['operand 1']} "
              f"{self.controller.kwargs['operator']} "
              f"{self.controller.kwargs['operand 2']} ?")
        print("Enter your answer or 'EXIT' to quit the program:")
        if err_msg:
            print(err_msg)
        user_input = input()
        self.controller.check_user_answer(user_input)

    def display_result(self, result, answer):
        if result:
            print(f"You answered {answer}. This is correct!")
        else:
            print(f"You answered {answer}. Wrong answer! The correct answer "
                  f"was {self.controller.kwargs['result']}")
        user_input = input("Press any key to continue or 'EXIT' to quit the "
                           "program:")
        print("\n")
        self.controller.check_question_navigation(user_input)

    def display_results_summary(self):
        print(f"Your score: {self.controller.current_score} / "
              f"{self.controller.current_question}")
        user_input = input("Press any key to return to the main menu or "
                           "'EXIT' to quit the program:")
        print("\n")
        self.controller.check_end_of_test_navigation(user_input)

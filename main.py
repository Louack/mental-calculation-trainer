from mvc.views import TkinterView, ConsoleView
from mvc.models import Addition, Multiplication
from mvc.controllers import TkinterController, ConsoleController

MAX_QUESTIONS: int = 10
OPERATIONS: dict = {
    "Addition": Addition(),
    "Multiplication": Multiplication()
}

if __name__ == "__main__":
    while True:
        print("Choose an interface:")
        print("1 - Console")
        print("2 - Tkinter")
        user_input = input()
        if user_input == "1":
            app = ConsoleController(
                view=ConsoleView(),
                operations=OPERATIONS,
                max_questions=MAX_QUESTIONS
            )
            app.start()
            break
        elif user_input == "2":
            app = TkinterController(
                view=TkinterView(),
                operations=OPERATIONS,
                max_questions=MAX_QUESTIONS
            )
            app.start()
            break



from mvc.views import TkView
from mvc.models import Addition, Multiplication
from mvc.controllers import Controller

MAX_QUESTIONS: int = 10
OPERATIONS: dict = {
    "Addition": Addition(),
    "Multiplication": Multiplication()
}

if __name__ == "__main__":
    app: Controller = Controller(
        view=TkView(),
        operations=OPERATIONS,
        max_questions=MAX_QUESTIONS
    )
    app.start()



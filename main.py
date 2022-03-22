from mvc.models import Addition, Multiplication
from factories import AppFactory, TkinterAppFactory, ConsoleAppFactory

MAX_QUESTIONS: int = 10
OPERATIONS: dict = {
    "Addition": Addition(),
    "Multiplication": Multiplication()
}


def get_user_input() -> AppFactory:
    """Returns an app factory according to a user input"""
    factories = {
        "1": ConsoleAppFactory(),
        "2": TkinterAppFactory()
    }
    while True:
        user_input = input(
            "Choose an interface:\n"
            "1 - Console\n"
            "2 - Tkinter\n"
        )
        if user_input in factories:
            break
    return factories[user_input]


def main(factory):
    """Builds and launch the app from the factory"""
    controller = factory.get_controller()
    view = factory.get_view()
    app = controller(
        view=view(),
        operations=OPERATIONS,
        max_questions=MAX_QUESTIONS
    )
    app.start()


if __name__ == "__main__":
    chosen_factory = get_user_input()
    main(chosen_factory)

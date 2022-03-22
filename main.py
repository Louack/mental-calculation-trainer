from mvc.models import Addition, Multiplication
from factories import AppFactory, TkinterAppFactory, ConsoleAppFactory


FACTORIES: dict = {
    "1": {
        "name": "Console",
        "factory": ConsoleAppFactory()
    },
    "2": {
        "name": "Tkinter",
        "factory": TkinterAppFactory()
    }
}

OPERATIONS: dict = {
    "Addition": Addition(),
    "Multiplication": Multiplication()
}

MAX_QUESTIONS: int = 10


def get_factory_from_user(factories: dict) -> AppFactory:
    """Returns an app factory according to a user input"""
    while True:
        print("Choose an interface:")
        for num, fact_dict in factories.items():
            print(f"{num} - {fact_dict['name']}")
        user_input = input()
        if user_input in factories:
            break
    return factories[user_input]["factory"]


def main(factory):
    """Builds and launch the app from the factory"""
    controller = factory.get_controller()
    view = factory.get_view()
    app = controller(
        view=view,
        operations=OPERATIONS,
        max_questions=MAX_QUESTIONS
    )
    app.start()


if __name__ == "__main__":
    chosen_factory = get_factory_from_user(FACTORIES)
    main(chosen_factory)

from abc import ABC, abstractmethod

from mvc.views import AbstractView, TkinterView, ConsoleView
from mvc.controllers import AbstractController, TkinterController, \
    ConsoleController


class AppFactory(ABC):
    """Provides the controller and the view need to build the app"""
    @abstractmethod
    def get_controller(self) -> AbstractController:
        """Provides a specific controller"""

    @abstractmethod
    def get_view(self) -> AbstractView:
        """Provides a specific view"""


class ConsoleAppFactory(AppFactory):
    """
    Provides a controller and a view allowing to run the app in the console
    """
    def get_controller(self):
        return ConsoleController

    def get_view(self):
        return ConsoleView()


class TkinterAppFactory(AppFactory):
    """
    Provides a controller and a view allowing to run the app in a tkinter GUI
    """
    def get_controller(self):
        return TkinterController

    def get_view(self):
        return TkinterView()

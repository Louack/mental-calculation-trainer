from abc import ABC, abstractmethod
from random import randint
from typing import Tuple


class Operation(ABC):
    """Abstract class for basic operation"""
    @property
    @abstractmethod
    def operator(self) -> str:
        """
        Defines the operator to be displayed in the text (X, /, +, -)
        """

    @abstractmethod
    def get_operands(self) -> Tuple[int, int]:
        """
        Returns two random operands
        """

    @abstractmethod
    def get_result(self, operand_1: int, operand_2: int) -> int:
        """
        return the operation result between two operands
        """


class Addition(Operation):
    operator: str = "+"

    def get_operands(self):
        return randint(1, 99), randint(1, 99)

    def get_result(self, operand_1, operand_2):
        return operand_1 + operand_2


class Multiplication(Operation):
    operator: str = "X"

    def get_operands(self):
        return randint(2, 9), randint(2, 9)

    def get_result(self, operand_1, operand_2):
        return operand_1 * operand_2

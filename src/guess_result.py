from enum import Enum


class GuessResult(Enum):
    CORRECT = "Correct"
    INCORRECT = "Incorrect"

    def __str__(self):
        return self.value

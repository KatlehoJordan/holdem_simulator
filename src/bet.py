from src.config import MIN_SMALL_BLIND


class Bet:
    def __init__(self, amount: int):
        if amount < MIN_SMALL_BLIND:
            raise ValueError(
                f"Amount must be greater than or equal to {MIN_SMALL_BLIND}"
            )
        self.amount = amount

    def __str__(self):
        return f"Bet: {self.amount}"

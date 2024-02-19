import random

from src.bet import Bet
from src.config import MAX_SMALL_BLIND, MIN_SMALL_BLIND, SMALL_BLIND_INCREMENT, logger


class SmallBlind(Bet):
    def __init__(self, amount: int):
        if amount > MAX_SMALL_BLIND or amount % SMALL_BLIND_INCREMENT != 0:
            raise ValueError(
                f"Amount must be less than or equal {MAX_SMALL_BLIND} and divisible by {SMALL_BLIND_INCREMENT}"
            )
        super().__init__(amount)
        logger.info(f"{self}")

    def __str__(self):
        return f"Small blind: {self.amount}"


def make_random_small_blind():
    num_increments = random.randint(
        MIN_SMALL_BLIND // SMALL_BLIND_INCREMENT,
        MAX_SMALL_BLIND // SMALL_BLIND_INCREMENT,
    )
    amount = num_increments * SMALL_BLIND_INCREMENT
    return SmallBlind(amount)

import random

from src.bet import Bet
from src.config import MIN_SMALL_BLIND, logger

# TODO: Modify this and big blind in order to train/simulate 10/10 games or 25/50 games, as they exist at Casino Cosmopol
SMALL_BLIND_INCREMENT = 5
MAX_SMALL_BLIND = 100


class SmallBlind(Bet):
    def __init__(
        self,
        amount: int,
        max_small_blind: int = MAX_SMALL_BLIND,
        small_blind_increment: int = SMALL_BLIND_INCREMENT,
    ):
        if amount > max_small_blind or amount % small_blind_increment != 0:
            raise ValueError(
                f"Amount must be less than or equal {max_small_blind} and divisible by {small_blind_increment}"
            )
        super().__init__(amount)
        logger.info("%s\n", self)

    def __str__(self):
        return f"Small blind: {self.amount}"

    @classmethod
    def select_random_small_blind(
        cls,
        min_small_blind: int = MIN_SMALL_BLIND,
        max_small_blind: int = MAX_SMALL_BLIND,
        small_blind_increment: int = SMALL_BLIND_INCREMENT,
    ) -> "SmallBlind":
        num_increments = random.randint(
            min_small_blind // small_blind_increment,
            max_small_blind // small_blind_increment,
        )
        amount = num_increments * small_blind_increment
        return cls(amount)

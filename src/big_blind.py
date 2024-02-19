from src.config import logger
from src.small_blind import SmallBlind, make_random_small_blind


class BigBlind:
    def __init__(self, small_blind: SmallBlind):
        self.amount = small_blind.amount * 2
        logger.info(f"{self}")

    def __str__(self):
        return f"Big blind: {self.amount}"


def make_big_blind():
    return BigBlind(make_random_small_blind())

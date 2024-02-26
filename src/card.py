from src.config import logger
from src.rank import Rank
from src.suit import Suit


class Card:
    def __init__(self, suit: Suit, rank: Rank):
        if not isinstance(suit, Suit):
            raise ValueError(f"suit must be a Suit, not {type(suit)}")
        if not isinstance(rank, Rank):
            raise ValueError(f"rank must be a Rank, not {type(rank)}")

        self.suit = suit
        self.rank = rank
        self.value = rank.final_rank_value
        self.name = f"{self.rank} of {self.suit}"

    def __str__(self):
        return f"{self.name}"

    def get_card_value(self):
        return logger.info(f"The card has value {self.value}")

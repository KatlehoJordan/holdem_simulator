from typing import List, Union

from src.config import VALID_RANKS_DICT, VALID_SUITS, logger
from src.rank import Rank
from src.suit import Suit

VALID_CARDS_DICT = {}


class Card:
    def __init__(self, suit: Union[Suit, None] = None, rank: Union[Rank, None] = None):
        if suit is None:
            suit = Suit.select_random_suit()
        if rank is None:
            rank = Rank.select_random_rank()
        if not isinstance(suit, Suit):
            raise ValueError(f"suit must be a Suit, not {type(suit)}")
        if not isinstance(rank, Rank):
            raise ValueError(f"rank must be a Rank, not {type(rank)}")

        self.suit = suit
        self.rank = rank
        self.value = rank.final_rank_value
        self.name = f"{self.rank} of {self.suit}"

    def __str__(self):
        return f"Card: {self.name}"

    def get_card_value(self):
        return logger.info(f"The card has value {self.value}")


def sort_cards_by_raw_rank_value(list_of_7_cards: List[Card]) -> List[int]:
    return sorted((card.rank.raw_rank_value for card in list_of_7_cards), reverse=True)


for suit in VALID_SUITS:
    for rank in VALID_RANKS_DICT.keys():
        card_name = f"{rank.upper()}_OF_{suit.upper()}"
        VALID_CARDS_DICT[card_name] = Card(Suit(suit), Rank(rank))

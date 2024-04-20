import pickle
from pathlib import Path
from typing import List, Union

from src.config import DATA_PATH, VALID_RANKS_DICT, VALID_SUITS, logger
from src.rank import Rank
from src.suit import Suit

VALID_CARDS_DICT = {}
VALID_CARDS_DICT_FILE_NAME = "valid_cards_dict.pkl"


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


def _make_valid_cards_dict(
    valid_suits: list[str] = VALID_SUITS,
    valid_ranks_dict: dict[str, dict[str, int]] = VALID_RANKS_DICT,
    data_path: Path = DATA_PATH,
    valid_cards_dict_file_name: str = VALID_CARDS_DICT_FILE_NAME,
) -> dict[str, Card]:
    pickle_file_path = Path(data_path) / valid_cards_dict_file_name

    if pickle_file_path.exists():
        logger.debug(f"Loading valid cards dict from {pickle_file_path}")
        with open(pickle_file_path, "rb") as f:
            valid_cards_dict = pickle.load(f)
        return valid_cards_dict
    else:
        logger.info(f"Saving valid cards dict to {pickle_file_path}")
        valid_cards_dict = {}
        for suit in valid_suits:
            for rank in valid_ranks_dict.keys():
                card_name = f"{rank.upper()}_OF_{suit.upper()}"
                valid_cards_dict[card_name] = Card(Suit(suit), Rank(rank))

        with open(pickle_file_path, "wb") as f:
            pickle.dump(valid_cards_dict, f)
        return valid_cards_dict


VALID_CARDS_DICT = _make_valid_cards_dict()

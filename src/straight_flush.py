from typing import List, Tuple

from src.card import Card
from src.flush import validate_flush
from src.straight import validate_straight

STRAIGHT_FLUSH_HAND_TYPE_SCORE = 8


class StraightFlush:
    def __init__(
        self,
        top_ranks_in_straight_flush: List[int],
        name: str,
        straight_flush_hand_type_score: int = STRAIGHT_FLUSH_HAND_TYPE_SCORE,
    ):
        self.hand_type_score = straight_flush_hand_type_score
        self.top_ranks = top_ranks_in_straight_flush
        self.name = name

    def __str__(self):
        return f"{self.name}"


def validate_straight_flush(list_of_7_cards: List[Card]) -> Tuple[bool, List[int], str]:
    flush_found, _, _, flush_cards, most_common_suit = validate_flush(list_of_7_cards)
    straight_found, top_ranks_in_straight_flush, _ = validate_straight(flush_cards)

    if flush_found and straight_found:
        straight_flush_found = True
    else:
        straight_flush_found = False

    name = f"Straight Flush, {top_ranks_in_straight_flush} high in {most_common_suit}."
    return straight_flush_found, top_ranks_in_straight_flush, name

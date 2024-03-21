from collections import Counter
from typing import List, Tuple

from src.card import Card
from src.flush import get_details_for_validating_flush, validate_flush
from src.straight import validate_straight

STRAIGHT_FLUSH_HAND_TYPE_SCORE = 8


def validate_straight_flush(
    list_of_7_cards: List[Card], hand_type_score: int = STRAIGHT_FLUSH_HAND_TYPE_SCORE
) -> Tuple[bool, int, List[int], str]:
    result_of_flush_validation = validate_flush(list_of_7_cards)

    if len(result_of_flush_validation) == 6:
        flush_found, _, _, _, flush_cards, most_common_suit = result_of_flush_validation
    else:
        flush_found, _, _, _ = result_of_flush_validation
        _, most_common_suit, flush_cards = get_details_for_validating_flush(
            list_of_7_cards
        )

    straight_found, _, top_ranks_in_straight_flush, _ = validate_straight(flush_cards)

    if flush_found and straight_found:
        straight_flush_found = True
        name = (
            f"Straight Flush: {top_ranks_in_straight_flush} high in {most_common_suit}."
        )
    else:
        straight_flush_found = False
        name = "No Straight Flush."

    return straight_flush_found, hand_type_score, top_ranks_in_straight_flush, name

from typing import List, Tuple

from src.card import Card, sort_cards_by_raw_rank_value
from src.config import NUMBER_OF_CARDS_IN_QUALIFYING_HAND

HI_CARD_HAND_TYPE_SCORE = 0


def validate_hi_card(
    list_of_7_cards: List[Card],
    hand_type_score: int = HI_CARD_HAND_TYPE_SCORE,
    n_cards_in_qualifying_hand: int = NUMBER_OF_CARDS_IN_QUALIFYING_HAND,
) -> Tuple[bool, int, List[int], str]:

    sorted_raw_rank_values = sort_cards_by_raw_rank_value(list_of_7_cards)

    n_kickers = n_cards_in_qualifying_hand

    hi_card_found = True
    top_ranks_in_hi_card = sorted_raw_rank_values[:n_cards_in_qualifying_hand]

    name = f"Hi cards, {top_ranks_in_hi_card[:n_kickers]}."
    return hi_card_found, hand_type_score, top_ranks_in_hi_card, name

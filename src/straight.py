from typing import List, Tuple

from src.card import Card, sort_cards_by_raw_rank_value
from src.config import (
    ACE_AS_HIGH_RAW_RANK_VALUE,
    ACE_AS_LOW_RAW_RANK_VALUE,
    NUMBER_OF_CARDS_IN_QUALIFYING_HAND,
    logger,
)

STRAIGHT_HAND_TYPE_SCORE = 4


def validate_straight(
    list_of_7_cards: List[Card],
    n_cards_in_a_straight: int = NUMBER_OF_CARDS_IN_QUALIFYING_HAND,
    low_ace_value: int = ACE_AS_LOW_RAW_RANK_VALUE,
    high_ace_value: int = ACE_AS_HIGH_RAW_RANK_VALUE,
    hand_type_score: int = STRAIGHT_HAND_TYPE_SCORE,
) -> Tuple[bool, int, List[int], str]:
    sorted_raw_rank_values = sort_cards_by_raw_rank_value(list_of_7_cards)

    if max(sorted_raw_rank_values) == high_ace_value:
        logger.debug("Ace can be high or low, so adding a low ace to the list.")
        sorted_raw_rank_values = sorted_raw_rank_values + [low_ace_value]

    current_n_cards_towards_a_straight = 1
    rank_of_max_card_in_straight = sorted_raw_rank_values[0]
    straight_found = False

    for current_rank, next_rank in zip(
        sorted_raw_rank_values[0:-1], sorted_raw_rank_values[1:]
    ):
        if current_rank == (next_rank + 1):
            current_n_cards_towards_a_straight += 1
            if current_n_cards_towards_a_straight == n_cards_in_a_straight:
                straight_found = True
                break
        else:
            current_n_cards_towards_a_straight = 1
            rank_of_max_card_in_straight = next_rank

    logger.debug(f"Max card in straight is {rank_of_max_card_in_straight}.")

    index_of_max_card = sorted_raw_rank_values.index(rank_of_max_card_in_straight)
    top_ranks_in_straight = sorted_raw_rank_values[
        index_of_max_card : n_cards_in_a_straight + 1
    ]
    logger.debug(f"Top ranks in straight are {top_ranks_in_straight}.")

    name = f"Straight, {rank_of_max_card_in_straight} high."

    return straight_found, hand_type_score, top_ranks_in_straight, name

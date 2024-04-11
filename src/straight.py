from typing import List, Tuple

from src.card import Card, sort_cards_by_raw_rank_value
from src.config import (
    ACE_AS_HIGH_RAW_RANK_VALUE,
    ACE_AS_LOW_RAW_RANK_VALUE,
    NUMBER_OF_CARDS_IN_QUALIFYING_HAND,
    find_key_by_raw_rank_value,
    logger,
)

STRAIGHT_HAND_TYPE_SCORE = 4


def validate_straight(
    list_of_5_to_7_cards: List[Card],
    n_cards_in_a_straight: int = NUMBER_OF_CARDS_IN_QUALIFYING_HAND,
    low_ace_value: int = ACE_AS_LOW_RAW_RANK_VALUE,
    high_ace_value: int = ACE_AS_HIGH_RAW_RANK_VALUE,
    hand_type_score: int = STRAIGHT_HAND_TYPE_SCORE,
    hand_name_root: str = "Straight",
) -> Tuple[bool, int, List[int], str]:
    logger.debug(
        "This function may be called to validate a straight flush, so it will handle 5 to 7 cards."
    )
    sorted_raw_rank_values = sort_cards_by_raw_rank_value(list_of_5_to_7_cards)

    unique_sorted_raw_rank_values = []
    for item in sorted_raw_rank_values:
        if item not in unique_sorted_raw_rank_values:
            unique_sorted_raw_rank_values.append(item)

    if max(unique_sorted_raw_rank_values) == high_ace_value:
        logger.debug("Ace can be high or low, so adding a low ace to the list.")
        unique_sorted_raw_rank_values = unique_sorted_raw_rank_values + [low_ace_value]

    current_n_cards_towards_a_straight = 1
    rank_of_max_card_in_straight_as_int = unique_sorted_raw_rank_values[0]
    rank_of_max_card_in_straight_as_string = find_key_by_raw_rank_value(
        rank_of_max_card_in_straight_as_int
    )
    straight_found = False
    top_ranks_in_straight_as_int = []
    name = f"No {hand_name_root}."

    for current_rank, next_rank in zip(
        unique_sorted_raw_rank_values[0:-1], unique_sorted_raw_rank_values[1:]
    ):
        if current_rank == (next_rank + 1):
            current_n_cards_towards_a_straight += 1
            if current_n_cards_towards_a_straight == n_cards_in_a_straight:
                straight_found = True
                name = (
                    f"{hand_name_root}: {rank_of_max_card_in_straight_as_string} high."
                )
                logger.debug(f"Max card in straight is {current_rank}.")
                top_ranks_in_straight_as_int = [
                    current_rank - 3,
                    current_rank - 2,
                    current_rank - 1,
                    current_rank,
                    next_rank,
                ]
                break
        else:
            current_n_cards_towards_a_straight = 1
            rank_of_max_card_in_straight_as_int = next_rank

    return straight_found, hand_type_score, top_ranks_in_straight_as_int, name

from typing import List, Tuple

from src.card import Card
from src.config import logger


def validate_straight(list_of_7_cards: List[Card]) -> Tuple[bool, int, str]:
    sorted_raw_rank_values = sorted(
        card.rank.raw_rank_value for card in list_of_7_cards
    )

    if max(sorted_raw_rank_values) == 14:
        logger.debug("Ace can be high or low, so adding a low ace to the list.")
        sorted_raw_rank_values = [1] + sorted_raw_rank_values

    longest_n_cards_towards_straight = current_n_cards_towards_a_straight = 1
    rank_of_max_card_in_straight = sorted_raw_rank_values[0]
    for i in range(1, len(sorted_raw_rank_values)):
        if sorted_raw_rank_values[i] == sorted_raw_rank_values[i - 1] + 1:
            current_n_cards_towards_a_straight += 1
            if current_n_cards_towards_a_straight > longest_n_cards_towards_straight:
                longest_n_cards_towards_straight = current_n_cards_towards_a_straight
                rank_of_max_card_in_straight = sorted_raw_rank_values[i]
        else:
            current_n_cards_towards_a_straight = 1

    logger.debug(f"Longest straight is {longest_n_cards_towards_straight} cards long.")
    logger.debug(f"Max card in straight is {rank_of_max_card_in_straight}.")

    if longest_n_cards_towards_straight < 5:
        straight_found = False
    else:
        straight_found = True
    name = f"Straight, {rank_of_max_card_in_straight} high."

    return straight_found, rank_of_max_card_in_straight, name

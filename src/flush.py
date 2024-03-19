from collections import Counter
from typing import List, Tuple, Union

from src.card import Card, sort_cards_by_raw_rank_value
from src.config import NUMBER_OF_CARDS_IN_QUALIFYING_HAND, logger

FLUSH_HAND_TYPE_SCORE = 5


def validate_flush(
    list_of_7_cards: List[Card],
    n_cards_in_a_flush: int = NUMBER_OF_CARDS_IN_QUALIFYING_HAND,
    hand_type_score: int = FLUSH_HAND_TYPE_SCORE,
    validating_for_straight_flush: bool = False,
) -> Union[
    Tuple[bool, int, List[int], str], Tuple[bool, int, List[int], str, List[Card], str]
]:
    suit_counts, most_common_suit, flush_cards = get_details_for_validating_flush(list_of_7_cards)

    logger.debug(f"Flush suit is {most_common_suit}.")
    logger.debug(f"Flush cards are {', '.join(str(card) for card in flush_cards)}.")

    sorted_raw_rank_values = sort_cards_by_raw_rank_value(flush_cards)

    top_ranks_in_flush = sorted_raw_rank_values[:n_cards_in_a_flush]

    logger.debug(f"Top ranks in flush are {top_ranks_in_flush}.")

    if suit_counts[most_common_suit] < n_cards_in_a_flush:
        flush_found = False
    else:
        flush_found = True

    name = f"Flush, {', '.join(str(rank) for rank in sorted_raw_rank_values[-n_cards_in_a_flush:])}, in {most_common_suit}."

    if validating_for_straight_flush:
        return (
            flush_found,
            hand_type_score,
            top_ranks_in_flush,
            name,
            flush_cards,
            most_common_suit,
        )
    else:
        return (flush_found, hand_type_score, top_ranks_in_flush, name)

def get_details_for_validating_flush(list_of_7_cards: List[Card]) -> Tuple[Counter, str, List[Card]]:
    suits = [card.suit.name for card in list_of_7_cards]
    suit_counts = Counter(suits)
    most_common_suit = suit_counts.most_common(1)[0][0]

    flush_cards = [
        card for card in list_of_7_cards if card.suit.name == most_common_suit
    ]
    
    return suit_counts,most_common_suit,flush_cards

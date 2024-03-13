from collections import Counter
from typing import List, Tuple

from src.card import Card
from src.config import logger


def validate_flush(list_of_7_cards: List[Card]) -> Tuple[bool, str, List[Card], str]:
    suits = [card.suit.name for card in list_of_7_cards]
    suit_counts = Counter(suits)
    most_common_suit = suit_counts.most_common(1)[0][0]

    flush_cards = [
        card for card in list_of_7_cards if card.suit.name == most_common_suit
    ]

    logger.debug(f"Flush suit is {most_common_suit}.")
    logger.debug(f"Flush cards are {', '.join(str(card) for card in flush_cards)}.")

    if suit_counts[most_common_suit] < 5:
        flush_found = False
    else:
        flush_found = True
    sorted_raw_rank_values = sorted(
        card.rank.raw_rank_value for card in list_of_7_cards
    )
    name = f"Flush, {sorted_raw_rank_values[-1]}, {sorted_raw_rank_values[-2]}, {sorted_raw_rank_values[-3]}, {sorted_raw_rank_values[-4]}, {sorted_raw_rank_values[-5]}, in {most_common_suit}."

    return flush_found, most_common_suit, flush_cards, name

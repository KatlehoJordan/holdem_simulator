from collections import Counter
from typing import List, Tuple

from src.card import Card, sort_cards_by_raw_rank_value
from src.config import NUMBER_OF_CARDS_IN_QUALIFYING_HAND


def validate_n_of_a_kind(
    list_of_7_cards: List[Card],
    hand_name_root: str,
    hand_type_score: int,
    n_cards_in_n_of_a_kind: int,
    n_cards_in_qualifying_hand: int = NUMBER_OF_CARDS_IN_QUALIFYING_HAND,
) -> Tuple[bool, int, List[int], str]:
    raw_rank_values = Counter(card.rank.raw_rank_value for card in list_of_7_cards)

    sorted_raw_rank_values = sort_cards_by_raw_rank_value(list_of_7_cards)

    n_of_a_kind_found = any(
        count >= n_cards_in_n_of_a_kind for count in raw_rank_values.values()
    )

    n_kickers = n_cards_in_qualifying_hand - n_cards_in_n_of_a_kind

    if n_of_a_kind_found:
        n_of_a_kind_rank = max(
            (
                rank
                for rank, count in raw_rank_values.items()
                if count >= n_cards_in_n_of_a_kind
            )
        )
        top_ranks_in_n_of_a_kind = [n_of_a_kind_rank] * n_cards_in_n_of_a_kind

        remaining_ranks = [
            rank for rank in sorted_raw_rank_values if rank != n_of_a_kind_rank
        ]

        while (len(top_ranks_in_n_of_a_kind) < n_cards_in_qualifying_hand) and (
            len(remaining_ranks) > 0
        ):
            highest_remaining_rank = max(remaining_ranks)
            top_ranks_in_n_of_a_kind.append(highest_remaining_rank)
            remaining_ranks.remove(highest_remaining_rank)

        name = f"{hand_name_root}: {top_ranks_in_n_of_a_kind[0]}s with {top_ranks_in_n_of_a_kind[-n_kickers:]} kicker/s."
    else:
        top_ranks_in_n_of_a_kind = sorted_raw_rank_values[:n_cards_in_qualifying_hand]
        name = f"No {hand_name_root}."

    return n_of_a_kind_found, hand_type_score, top_ranks_in_n_of_a_kind, name

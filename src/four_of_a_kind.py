from collections import Counter
from typing import List, Tuple

from src.card import Card
from src.config import NUMBER_OF_CARDS_IN_QUALIFYING_HAND, logger

FOUR_OF_A_KIND_HAND_TYPE_SCORE = 7
N_CARDS_IN_FOUR_OF_A_KIND = 4


class FourOfAKind:

    def __init__(
        self,
        top_ranks_in_four_of_a_kind: List[int],
        name: str,
        four_of_a_kind_hand_type_score: int = FOUR_OF_A_KIND_HAND_TYPE_SCORE,
    ):
        self.hand_type_score = four_of_a_kind_hand_type_score
        self.top_ranks = top_ranks_in_four_of_a_kind
        self.name = name

    def __str__(self):
        return f"{self.name}"


def validate_four_of_a_kind(
    list_of_7_cards: List[Card],
    n_cards_in_a_four_of_a_kind: int = N_CARDS_IN_FOUR_OF_A_KIND,
    n_cards_in_qualifying_hand: int = NUMBER_OF_CARDS_IN_QUALIFYING_HAND,
) -> Tuple[bool, List[int], str]:
    # TODO: generalize this for any N of a kind...g
    raw_rank_values = Counter(card.rank.raw_rank_value for card in list_of_7_cards)

    sorted_raw_rank_values = sorted(
        (card.rank.raw_rank_value for card in list_of_7_cards), reverse=True
    )

    four_of_a_kind_found = any(
        count == n_cards_in_a_four_of_a_kind for count in raw_rank_values.values()
    )

    n_kickers = n_cards_in_qualifying_hand - n_cards_in_a_four_of_a_kind

    if four_of_a_kind_found:
        four_of_a_kind_rank = next(
            (
                rank
                for rank, count in raw_rank_values.items()
                if count == n_cards_in_a_four_of_a_kind
            )
        )
        top_ranks_in_four_of_a_kind = [
            four_of_a_kind_rank
        ] * n_cards_in_a_four_of_a_kind

        highest_remaining_rank = max(
            rank for rank in sorted_raw_rank_values if rank != four_of_a_kind_rank
        )

        top_ranks_in_four_of_a_kind.append(highest_remaining_rank)
    else:
        top_ranks_in_four_of_a_kind = sorted_raw_rank_values[
            :n_cards_in_qualifying_hand
        ]

    name = f"Four of a Kind, {top_ranks_in_four_of_a_kind[0]} with {top_ranks_in_four_of_a_kind[-n_kickers:]} kicker."
    return four_of_a_kind_found, top_ranks_in_four_of_a_kind, name

from typing import List, Tuple

from src.card import Card
from src.n_of_a_kind import validate_n_of_a_kind

THREE_OF_A_KIND_HAND_TYPE_SCORE = 3
N_CARDS_IN_THREE_OF_A_KIND = 3


def validate_three_of_a_kind(
    list_of_7_cards: List[Card],
    hand_name_base="Three of a Kind",
    hand_type_score=THREE_OF_A_KIND_HAND_TYPE_SCORE,
    n_cards_in_n_of_a_kind=N_CARDS_IN_THREE_OF_A_KIND,
) -> Tuple[bool, int, List[int], str]:
    n_of_a_kind_found, hand_type_score, top_ranks_in_n_of_a_kind, name = (
        validate_n_of_a_kind(
            list_of_7_cards=list_of_7_cards,
            hand_name_root=hand_name_base,
            hand_type_score=hand_type_score,
            n_cards_in_n_of_a_kind=n_cards_in_n_of_a_kind,
        )
    )
    return n_of_a_kind_found, hand_type_score, top_ranks_in_n_of_a_kind, name

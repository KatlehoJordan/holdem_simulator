from typing import List, Tuple

from src.card import Card
from src.pair import N_CARDS_IN_PAIR, validate_pair
from src.three_of_a_kind import N_CARDS_IN_THREE_OF_A_KIND, validate_three_of_a_kind

FULL_HOUSE_HAND_TYPE_SCORE = 6


def validate_full_house(
    list_of_7_cards: List[Card],
    hand_type_score: int = FULL_HOUSE_HAND_TYPE_SCORE,
    hand_name_root: str = "Full House",
) -> Tuple[bool, int, List[int], str]:
    result_of_three_of_a_kind_validation = validate_three_of_a_kind(list_of_7_cards)

    three_of_a_kind_found, _, top_ranks_in_three_of_a_kind, _ = (
        result_of_three_of_a_kind_validation
    )
    three_of_a_kind_rank = top_ranks_in_three_of_a_kind[0]

    remaining_cards = [
        card
        for card in list_of_7_cards
        if card.rank.raw_rank_value != three_of_a_kind_rank
    ]
    result_of_pair_validation = validate_pair(remaining_cards)
    pair_found, _, top_ranks_in_pair, _ = result_of_pair_validation
    pair_rank = top_ranks_in_pair[0]

    if three_of_a_kind_found and pair_found:
        full_house_found = True
        top_ranks_in_full_house = (
            top_ranks_in_three_of_a_kind[0:N_CARDS_IN_THREE_OF_A_KIND]
            + top_ranks_in_pair[0:N_CARDS_IN_PAIR]
        )
        name = f"{hand_name_root}: {three_of_a_kind_rank}s over {pair_rank}s."
    else:
        full_house_found = False
        top_ranks_in_full_house = []
        name = "No {hand_name_root}."

    return full_house_found, hand_type_score, top_ranks_in_full_house, name

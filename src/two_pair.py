from typing import List, Tuple

from src.card import Card
from src.pair import N_CARDS_IN_PAIR, validate_pair

TWO_PAIR_HAND_TYPE_SCORE = 2


def validate_two_pair(
    list_of_7_cards: List[Card],
    hand_type_score: int = TWO_PAIR_HAND_TYPE_SCORE,
    hand_name_root: str = "Two Pair",
) -> Tuple[bool, int, List[int], str]:
    result_of_first_pair_validation = validate_pair(list_of_7_cards)

    first_pair_found, _, top_ranks_in_first_pair, _ = result_of_first_pair_validation
    first_pair_rank = top_ranks_in_first_pair[0]

    remaining_cards = [
        card for card in list_of_7_cards if card.rank.raw_rank_value != first_pair_rank
    ]
    second_pair_found, _, top_ranks_in_second_pair, _ = validate_pair(remaining_cards)
    second_pair_rank = top_ranks_in_second_pair[0]

    if first_pair_found and second_pair_found:
        two_pair_found = True
        top_ranks_in_two_pair = (
            top_ranks_in_first_pair[0:N_CARDS_IN_PAIR]
            + top_ranks_in_second_pair[0:N_CARDS_IN_PAIR]
        )
        name = f"{hand_name_root}: {first_pair_rank}s over {second_pair_rank}s."
    else:
        two_pair_found = False
        top_ranks_in_two_pair = []
        name = f"No {hand_name_root}."

    return two_pair_found, hand_type_score, top_ranks_in_two_pair, name

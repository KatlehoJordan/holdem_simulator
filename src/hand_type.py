from typing import List

FOUR_OF_A_KIND_HAND_TYPE_SCORE = 7
N_CARDS_IN_FOUR_OF_A_KIND = 4
STRAIGHT_FLUSH_HAND_TYPE_SCORE = 8


class HandType:
    def __init__(
        self,
        hand_type_score: int,
        top_ranks: List[int],
        name: str,
    ):
        self.hand_type_score = hand_type_score
        self.top_ranks = top_ranks
        self.name = name

    def __str__(self):
        return f"{self.name}"

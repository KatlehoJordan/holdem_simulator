from typing import List


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

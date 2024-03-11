STRAIGHT_FLUSH_HAND_TYPE_SCORE = 8


class StraightFlush:
    def __init__(
        self,
        high_card_raw_rank_value: int,
        name: str,
        straight_flush_hand_type_score: int = STRAIGHT_FLUSH_HAND_TYPE_SCORE,
    ):
        self.hand_type_score = straight_flush_hand_type_score
        self.high_card_raw_rank_value = high_card_raw_rank_value
        self.name = name

    def __str__(self):
        return f"{self.name}"

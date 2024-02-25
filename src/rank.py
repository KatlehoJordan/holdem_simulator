from typing import Dict

RAW_RANK_VALUE_STRING = "raw_rank_value"
N_POSSIBLE_STRAIGHTS_STRING = "n_possible_straights"

VALID_RANKS_DICT = {
    "2": {
        RAW_RANK_VALUE_STRING: 2,
        N_POSSIBLE_STRAIGHTS_STRING: 2,
    },
    "3": {
        RAW_RANK_VALUE_STRING: 3,
        N_POSSIBLE_STRAIGHTS_STRING: 3,
    },
    "4": {
        RAW_RANK_VALUE_STRING: 4,
        N_POSSIBLE_STRAIGHTS_STRING: 4,
    },
    "5": {
        RAW_RANK_VALUE_STRING: 5,
        N_POSSIBLE_STRAIGHTS_STRING: 5,
    },
    "6": {
        RAW_RANK_VALUE_STRING: 6,
        N_POSSIBLE_STRAIGHTS_STRING: 5,
    },
    "7": {
        RAW_RANK_VALUE_STRING: 7,
        N_POSSIBLE_STRAIGHTS_STRING: 5,
    },
    "8": {
        RAW_RANK_VALUE_STRING: 8,
        N_POSSIBLE_STRAIGHTS_STRING: 5,
    },
    "9": {
        RAW_RANK_VALUE_STRING: 9,
        N_POSSIBLE_STRAIGHTS_STRING: 5,
    },
    "10": {
        RAW_RANK_VALUE_STRING: 10,
        N_POSSIBLE_STRAIGHTS_STRING: 5,
    },
    "Jack": {
        RAW_RANK_VALUE_STRING: 11,
        N_POSSIBLE_STRAIGHTS_STRING: 4,
    },
    "Queen": {
        RAW_RANK_VALUE_STRING: 12,
        N_POSSIBLE_STRAIGHTS_STRING: 3,
    },
    "King": {
        RAW_RANK_VALUE_STRING: 13,
        N_POSSIBLE_STRAIGHTS_STRING: 2,
    },
    "Ace": {
        RAW_RANK_VALUE_STRING: 14,
        N_POSSIBLE_STRAIGHTS_STRING: 2,
    },
}

RAW_RANK_WEIGHT_FACTOR = 1.111
N_STRAIGHTS_WEIGHT_FACTOR = 1.0


class Rank:
    def __init__(
        self,
        rank: str,
        valid_ranks_dict: Dict[str, Dict[str, int]] = VALID_RANKS_DICT,
        raw_rank_value_string: str = RAW_RANK_VALUE_STRING,
        raw_rank_weight_factor: float = RAW_RANK_WEIGHT_FACTOR,
        n_possible_straights_string: str = N_POSSIBLE_STRAIGHTS_STRING,
        n_straights_weight_factor: float = N_STRAIGHTS_WEIGHT_FACTOR,
    ):
        if rank not in valid_ranks_dict.keys():
            raise ValueError(f"Rank must be one of {valid_ranks_dict.keys()}")

        self.rank = rank

        self.raw_rank_value = valid_ranks_dict[rank][raw_rank_value_string]
        min_raw_rank_value = min(
            [value[raw_rank_value_string] for value in valid_ranks_dict.values()]
        )
        raw_rank_diff = self.raw_rank_value - min_raw_rank_value
        self.adjusted_raw_rank_value = raw_rank_diff * (
            raw_rank_weight_factor**raw_rank_diff
        )

        self.n_possible_straights = valid_ranks_dict[rank][n_possible_straights_string]
        min_n_possible_straights = min(
            [value[n_possible_straights_string] for value in valid_ranks_dict.values()]
        )
        n_possible_straights_diff = self.n_possible_straights - min_n_possible_straights
        self.adjusted_n_possible_straights = n_possible_straights_diff * (
            n_straights_weight_factor**n_possible_straights_diff
        )

        self.final_rank_value = int(
            self.adjusted_raw_rank_value + self.adjusted_n_possible_straights
        )

    def __str__(self):
        return f"Rank is: {self.rank}; final rank value is: {self.final_rank_value}"

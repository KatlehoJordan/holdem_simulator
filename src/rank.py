import random
from typing import Dict

from src.config import (
    N_POSSIBLE_STRAIGHTS_STRING,
    RAW_RANK_VALUE_STRING,
    VALID_RANKS_DICT,
)

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

        self.final_rank_value = round(
            self.adjusted_raw_rank_value + self.adjusted_n_possible_straights
        )

    def __str__(self):
        return f"{self.rank}"

    @classmethod
    def select_random_rank(
        cls, valid_ranks_dict: Dict[str, Dict[str, int]] = VALID_RANKS_DICT
    ) -> "Rank":
        return cls(random.choice(list(valid_ranks_dict.keys())))

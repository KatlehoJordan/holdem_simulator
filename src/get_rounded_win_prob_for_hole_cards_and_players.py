import pickle
from pathlib import Path

import pandas as pd

from src.config import DATA_PATH, PICKLE_FILE_SAVE_TYPE, logger
from src.get_wins_by_hole_cards_flavor_data import get_wins_by_hole_cards_flavor_df
from src.make_round_to_percent_string import make_round_to_percent_string

ROUNDED_FILE_STEM = "rounded_win_prob_for_hole_cards_and_players_"


def get_rounded_win_prob_for_hole_cards_and_players() -> pd.DataFrame:
    pickle_file_path = _make_pickle_file_path()

    if pickle_file_path.exists():
        logger.debug(
            f"Loading rounded_win_prob_for_hole_cards_and_players from {pickle_file_path}"
        )
        with open(pickle_file_path, "rb") as f:
            rounded_win_prob_for_hole_cards_and_players_df = pickle.load(f)
        return rounded_win_prob_for_hole_cards_and_players_df
    else:
        logger.info(
            f"Saving rounded_win_prob_for_hole_cards_and_players_df to {pickle_file_path}"
        )
        percent_rounded_down_to_str = make_round_to_percent_string()
        rounded_win_prob_for_hole_cards_and_players_df = pd.DataFrame()
        wins_by_hole_cards_flavor_df = get_wins_by_hole_cards_flavor_df()
        rounded_win_prob_for_hole_cards_and_players_df = wins_by_hole_cards_flavor_df[
            [
                "hole cards flavor",
                f"win ratio rounded down to nearest {percent_rounded_down_to_str}",
                "n_players",
            ]
        ]

        with open(pickle_file_path, "wb") as f:
            pickle.dump(rounded_win_prob_for_hole_cards_and_players_df, f)
        return rounded_win_prob_for_hole_cards_and_players_df


def _make_pickle_file_path(
    data_path: Path = DATA_PATH,
    rounded_file_stem: str = ROUNDED_FILE_STEM,
    pickle_file_save_type: str = PICKLE_FILE_SAVE_TYPE,
) -> Path:
    percent_rounded_down_to_str = make_round_to_percent_string()[:-1]

    pickle_file_path = (
        Path(data_path)
        / f"{rounded_file_stem}{percent_rounded_down_to_str}{pickle_file_save_type}"
    )

    return pickle_file_path

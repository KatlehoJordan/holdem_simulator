import pickle
from pathlib import Path

import pandas as pd

from src.config import DATA_PATH, PICKLE_FILE_SAVE_TYPE, logger
from src.get_wins_by_hole_cards_flavor_data import get_wins_by_hole_cards_flavor_df

ROUNDED_WIN_PROB_FOR_HOLE_CARDS_AND_PLAYERS_DATA_FILE_NAME = (
    f"rounded_win_prob_for_hole_cards_and_players{PICKLE_FILE_SAVE_TYPE}"
)


def get_rounded_win_prob_for_hole_cards_and_players(
    data_path: Path = DATA_PATH,
    rounded_win_prob_for_hole_cards_and_players_file_name: str = ROUNDED_WIN_PROB_FOR_HOLE_CARDS_AND_PLAYERS_DATA_FILE_NAME,
) -> pd.DataFrame:
    pickle_file_path = (
        Path(data_path) / rounded_win_prob_for_hole_cards_and_players_file_name
    )

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
        rounded_win_prob_for_hole_cards_and_players_df = pd.DataFrame()
        rounded_win_prob_for_hole_cards_and_players_df = (
            get_wins_by_hole_cards_flavor_df()
        )
        rounded_win_prob_for_hole_cards_and_players_df = (
            rounded_win_prob_for_hole_cards_and_players_df[
                [
                    "hole cards flavor",
                    "win ratio rounded down to nearest 5%",
                    "n_players",
                ]
            ]
        )

        with open(pickle_file_path, "wb") as f:
            pickle.dump(rounded_win_prob_for_hole_cards_and_players_df, f)
        return rounded_win_prob_for_hole_cards_and_players_df

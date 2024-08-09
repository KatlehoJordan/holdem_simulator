import pickle
from pathlib import Path

import pandas as pd

from src.config import (
    DATA_PATH,
    N_PLAYERS_STRING,
    N_POSSIBLE_PLAYERS,
    PICKLE_FILE_SAVE_TYPE,
    logger,
)
from src.load_wins_by_hole_cards_flavor_df import load_wins_by_hole_cards_flavor_df
from src.make_round_to_percent_string import make_round_to_percent_string

WINS_BY_HOLE_CARDS_FLAVOR_FILE_NAME_STEM = "wins_by_hole_cards_flavor_"


def get_wins_by_hole_cards_flavor_df(
    n_possible_players: list[int] = N_POSSIBLE_PLAYERS,
    n_players_string: str = N_PLAYERS_STRING,
) -> pd.DataFrame:
    pickle_file_path = _make_pickle_file_path()

    if pickle_file_path.exists():
        logger.debug(f"Loading wins_by_hole_cards_flavor_df from {pickle_file_path}")
        with open(pickle_file_path, "rb") as f:
            wins_by_hole_cards_flavor_df = pickle.load(f)
        return wins_by_hole_cards_flavor_df
    else:
        logger.info(f"Saving wins_by_hole_cards_flavor_df to {pickle_file_path}")
        wins_by_hole_cards_flavor_df = pd.DataFrame()
        for players in n_possible_players:
            ith_df = load_wins_by_hole_cards_flavor_df(n_players_to_plot=players)
            ith_df[n_players_string] = players
            wins_by_hole_cards_flavor_df = pd.concat(
                [wins_by_hole_cards_flavor_df, ith_df]
            )

        with open(pickle_file_path, "wb") as f:
            pickle.dump(wins_by_hole_cards_flavor_df, f)
        return wins_by_hole_cards_flavor_df


def _make_pickle_file_path(
    data_path: Path = DATA_PATH,
) -> Path:
    wins_by_hole_cards_flavor_file_name = (
        _make_wins_by_hole_cards_flavor_data_file_name()
    )
    pickle_file_path = Path(data_path) / wins_by_hole_cards_flavor_file_name
    return pickle_file_path


def _make_wins_by_hole_cards_flavor_data_file_name(
    name_stem: str = WINS_BY_HOLE_CARDS_FLAVOR_FILE_NAME_STEM,
    pickle_file_save_type: str = PICKLE_FILE_SAVE_TYPE,
) -> str:
    percent_string = make_round_to_percent_string()[:-1]
    return f"{name_stem}{percent_string}{pickle_file_save_type}"

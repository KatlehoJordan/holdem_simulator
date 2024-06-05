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

WINS_BY_HOLE_CARDS_FLAVOR_DATA_FILE_NAME = (
    f"wins_by_hole_cards_flavor{PICKLE_FILE_SAVE_TYPE}"
)


def get_wins_by_hole_cards_flavor_df(
    data_path: Path = DATA_PATH,
    wins_by_hole_cards_flavor_file_name: str = WINS_BY_HOLE_CARDS_FLAVOR_DATA_FILE_NAME,
    n_possible_players: list[int] = N_POSSIBLE_PLAYERS,
    n_players_string: str = N_PLAYERS_STRING,
) -> pd.DataFrame:
    pickle_file_path = Path(data_path) / wins_by_hole_cards_flavor_file_name

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

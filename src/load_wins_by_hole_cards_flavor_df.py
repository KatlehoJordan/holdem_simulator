from pathlib import Path

import pandas as pd

from src.aggregate_simulations import (
    PATH_TO_AGGREGATED_DATA_RESULTS,
    WINS_BY_HOLE_CARDS_FLAVOR_STRING,
)
from src.config import FILE_SAVE_TYPE, logger
from src.get_path_for_n_players_aggregated import get_path_for_n_players_aggregated


def load_wins_by_hole_cards_flavor_df(
    n_players_to_plot: int,
    path_to_aggregated_directory: Path = PATH_TO_AGGREGATED_DATA_RESULTS,
    wins_by_hole_cards_flavor_string: str = WINS_BY_HOLE_CARDS_FLAVOR_STRING,
    file_save_type: str = FILE_SAVE_TYPE,
) -> pd.DataFrame:
    path_for_n_players = get_path_for_n_players_aggregated(
        n_players_simulated_to_aggregate=n_players_to_plot
    )
    path_for_n_players_aggregated = path_for_n_players / path_to_aggregated_directory
    logger.debug(
        f"Getting data from {path_for_n_players_aggregated} to make dataframe."
    )
    file_name = f"{wins_by_hole_cards_flavor_string}{file_save_type}"
    file_path_for_results = path_for_n_players_aggregated / file_name
    return pd.read_csv(file_path_for_results)

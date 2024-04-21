import importlib
from pathlib import Path
from typing import Union

import pandas as pd
from pandas import DataFrame

import src.plot_builders_plotly
from src.aggregate_simulations import (
    PATH_TO_AGGREGATED_DATA_RESULTS,
    WINS_BY_HOLE_CARDS_FLAVOR_STRING,
)
from src.config import FILE_SAVE_TYPE, N_PLAYERS_TO_SIM_AGG_OR_PLOT
from src.get_path_for_n_players_aggregated import get_path_for_n_players_aggregated
from src.plot_builders_mpl import use_mpl
from src.plot_builders_plotly import use_plotly

importlib.reload(src.plot_builders_plotly)


def plot_data(
    plot_engine: str = "plotly",
    n_players_to_plot: int = N_PLAYERS_TO_SIM_AGG_OR_PLOT,
    n_cols_to_show: Union[int, None] = None,
    show_plot: bool = False,
    save_plot: bool = False,
) -> None:
    wins_by_hole_cards_flavor_df = _load_wins_by_hole_cards_flavor_df(
        n_players_to_plot=n_players_to_plot
    )
    if plot_engine == "plotly":
        use_plotly(
            n_players_to_plot,
            n_cols_to_show,
            show_plot,
            save_plot,
            wins_by_hole_cards_flavor_df,
        )
    elif plot_engine == "mpl":
        use_mpl(n_cols_to_show, show_plot, save_plot, wins_by_hole_cards_flavor_df)


def _load_wins_by_hole_cards_flavor_df(
    n_players_to_plot: int,
    path_to_aggregated_directory: Path = PATH_TO_AGGREGATED_DATA_RESULTS,
    wins_by_hole_cards_flavor_string: str = WINS_BY_HOLE_CARDS_FLAVOR_STRING,
    file_save_type: str = FILE_SAVE_TYPE,
) -> DataFrame:
    path_for_n_players = get_path_for_n_players_aggregated(
        n_players_simulated_to_aggregate=n_players_to_plot
    )
    path_for_n_players_aggregated = path_for_n_players / path_to_aggregated_directory
    file_name = f"{wins_by_hole_cards_flavor_string}{file_save_type}"
    file_path_for_results = path_for_n_players_aggregated / file_name
    return pd.read_csv(file_path_for_results)

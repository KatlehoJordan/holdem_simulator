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
from src.config import (
    FILE_SAVE_TYPE,
    N_PLAYERS_STRING,
    N_PLAYERS_TO_SIM_AGG_OR_PLOT,
    N_POSSIBLE_PLAYERS,
)
from src.get_path_for_n_players_aggregated import get_path_for_n_players_aggregated
from src.plot_builders_mpl import use_mpl
from src.plot_builders_plotly import (
    ACCEPTABLE_N_PLAYERS_TO_PLOT,
    PLOT_ALL_PLAYERS_STRING,
    use_plotly,
)

importlib.reload(src.plot_builders_plotly)

PLOTLY_STRING = "plotly"
MATPLOTLIB_STRING = "mpl"
ACCEPTABLE_PLOT_ENGINES = [PLOTLY_STRING, MATPLOTLIB_STRING]


def plot_data(
    plot_engine: str = PLOTLY_STRING,
    n_players_to_plot: Union[int, str] = N_PLAYERS_TO_SIM_AGG_OR_PLOT,
    n_players_string: str = N_PLAYERS_STRING,
    n_cols_to_show: Union[int, None] = None,
    show_plot: bool = False,
    save_plot: bool = False,
    acceptable_n_possible_players: list[int | str] = ACCEPTABLE_N_PLAYERS_TO_PLOT,
    plot_all_players_string: str = PLOT_ALL_PLAYERS_STRING,
    acceptable_plot_engines: list[str] = ACCEPTABLE_PLOT_ENGINES,
    plotly_string: str = PLOTLY_STRING,
    mpl_string: str = MATPLOTLIB_STRING,
) -> None:
    if n_players_to_plot not in acceptable_n_possible_players:
        raise ValueError(
            f"{n_players_string}_to_plot must be one of {acceptable_n_possible_players}"
        )
    if plot_engine not in acceptable_plot_engines:
        raise ValueError(f"plot_engine must be one of {acceptable_plot_engines}")
    if n_players_to_plot == plot_all_players_string:
        df_to_plot = _load_all_players_wins_by_hole_cards_flavor_df()
    else:
        wins_by_hole_cards_flavor_df = _load_wins_by_hole_cards_flavor_df(
            n_players_to_plot=int(n_players_to_plot)
        )
        df_to_plot = wins_by_hole_cards_flavor_df
    if plot_engine == plotly_string:
        use_plotly(
            n_players_to_plot,
            show_plot,
            save_plot,
            df_to_plot,
        )
    elif plot_engine == mpl_string:
        use_mpl(
            n_cols_to_show,
            show_plot,
            save_plot,
            df_to_plot,
        )


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


# TODO: Continue working from here
def _load_all_players_wins_by_hole_cards_flavor_df(
    n_possible_players: list[int] = N_POSSIBLE_PLAYERS,
    n_players_string: str = N_PLAYERS_STRING,
) -> DataFrame:
    stacked_df = pd.DataFrame()
    for players in n_possible_players:
        wins_by_hole_cards_flavor_df = _load_wins_by_hole_cards_flavor_df(
            n_players_to_plot=players
        )
        wins_by_hole_cards_flavor_df[n_players_string] = players
        stacked_df = pd.concat([stacked_df, wins_by_hole_cards_flavor_df])
    return stacked_df

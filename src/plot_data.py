from pathlib import Path
from typing import Tuple, Union

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import DataFrame

from src.aggregate_simulations import (
    APPEARANCES_STRING,
    HOLE_CARDS_FLAVOR_STRING,
    PATH_TO_AGGREGATED_DATA_RESULTS,
    WIN_RATIO_ROUNDED_DOWN_STRING,
    WINS_BY_HOLE_CARDS_FLAVOR_STRING,
)
from src.config import FILE_SAVE_TYPE, N_PLAYERS_TO_SIM_AGG_OR_PLOT, logger
from src.get_path_for_n_players_aggregated import get_path_for_n_players_aggregated
from src.make_dir_if_does_not_exist import make_dir_if_not_exist

STYLES_PATH = Path("styles")
STYLES_FILE = "dgl_stylesheet.mpltstyle"
PATH_TO_STYLES = STYLES_PATH / STYLES_FILE
PLOTS_PATH = Path("plots")
PLOT_FILE_TYPE = ".svg"
PLOT_FILE_NAME = f"plot{PLOT_FILE_TYPE}"


def plot_data(
    n_players_to_plot: int = N_PLAYERS_TO_SIM_AGG_OR_PLOT,
    n_cols_to_show: Union[int, None] = None,
    show_plot: bool = False,
    save_plot: bool = False,
) -> None:
    wins_by_hole_cards_flavor_df = _load_wins_by_hole_cards_flavor_df(
        n_players_to_plot=n_players_to_plot
    )
    _use_plot_style()
    fig, _, _ = _make_fig_and_ax_objects(
        wins_by_hole_cards_flavor_df, n_cols_to_show=n_cols_to_show
    )
    _show_plot(show_plot=show_plot)
    _save_plot(fig, save_plot=save_plot)


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


def _use_plot_style() -> None:
    logger.info("Using plot style %s", PATH_TO_STYLES)
    plt.style.use(PATH_TO_STYLES)


# TODO: Import the variables for the names of the dataframe columns and remove the hard-coding here.
def _make_fig_and_ax_objects(
    dataframe: DataFrame,
    n_cols_to_show: Union[int, None] = None,
    hole_cards_flavor_string: str = HOLE_CARDS_FLAVOR_STRING,
    win_ratio_rounded_down_string: str = WIN_RATIO_ROUNDED_DOWN_STRING,
    appearances_string: str = APPEARANCES_STRING,
) -> Tuple[Figure, Axes, Axes]:
    x_var = hole_cards_flavor_string
    y1_var = win_ratio_rounded_down_string
    y2_var = appearances_string
    logger.info("Sorting data frame descending by %s", y1_var)
    dataframe = dataframe.sort_values(by=y1_var, ascending=False)
    if n_cols_to_show is not None:
        dataframe = dataframe.head(n_cols_to_show)
    logger.info("Plotting results")
    x = dataframe[x_var]
    y1 = dataframe[y1_var]
    y2 = dataframe[y2_var]
    fig, ax1 = plt.subplots()

    ax1.bar(x, y1)

    ax2 = ax1.twinx()
    ax1.set_ylim(bottom=0, top=1)
    ax2.set_ylim(bottom=0, top=y2.max() * 1.1)
    ax2.plot(x, y2)

    for label in ax1.get_xticklabels():
        label.set_rotation(45)
    return fig, ax1, ax2


def _show_plot(show_plot: bool = False) -> None:
    if not show_plot:
        logger.info("Not showing plot object - pass show_plot=True to show it.")
        return
    logger.info("Showing plot object")
    plt.show()


def _save_plot(
    fig: Figure,
    save_plot: bool = False,
    graph_file_name: str = PLOT_FILE_NAME,
    graphs_path: Path = PLOTS_PATH,
) -> None:
    if not save_plot:
        logger.info("Not saving plot - pass save_plot=True to save it.")
        return
    logger.info("Saving plot to %s", graphs_path / graph_file_name)
    make_dir_if_not_exist(graphs_path)
    fig.savefig(graphs_path / graph_file_name)
    plt.close(fig)

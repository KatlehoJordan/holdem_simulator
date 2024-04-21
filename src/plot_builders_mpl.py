from pathlib import Path
from typing import Tuple, Union

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import DataFrame

from src.aggregate_simulations import (
    APPEARANCES_STRING,
    HOLE_CARDS_FLAVOR_STRING,
    WIN_RATIO_ROUNDED_DOWN_STRING,
)
from src.config import PLOT_FILE_NAME, PLOTS_PATH, logger
from src.make_dir_if_does_not_exist import make_dir_if_not_exist

STYLES_PATH = Path("styles")
STYLES_FILE = "dgl_stylesheet.mpltstyle"
PATH_TO_STYLES = STYLES_PATH / STYLES_FILE


def use_mpl(n_cols_to_show, show_plot, save_plot, wins_by_hole_cards_flavor_df):
    _use_mpl_plot_style()
    fig, _, _ = _make_mpl_fig_and_ax_objects(
        wins_by_hole_cards_flavor_df, n_cols_to_show=n_cols_to_show
    )
    _show_mpl_plot(show_plot=show_plot)
    _save_mpl_plot(fig, save_plot=save_plot)


def _use_mpl_plot_style() -> None:
    logger.info("Using plot style %s", PATH_TO_STYLES)
    plt.style.use(PATH_TO_STYLES)


def _make_mpl_fig_and_ax_objects(
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


def _show_mpl_plot(show_plot: bool = False) -> None:
    if not show_plot:
        logger.info("Not showing plot object - pass show_plot=True to show it.")
        return
    logger.info("Showing plot object")
    plt.show()


def _save_mpl_plot(
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

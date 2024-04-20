from pathlib import Path
from typing import Tuple

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from src.config import N_PLAYERS_TO_SIM_AGG_OR_PLOT, logger
from src.make_dir_if_does_not_exist import make_dir_if_not_exist

STYLES_PATH = Path("styles")
STYLES_FILE = "dgl_stylesheet.mpltstyle"
PATH_TO_STYLES = STYLES_PATH / STYLES_FILE
PLOTS_PATH = Path("plots")
PLOT_FILE_TYPE = ".svg"
PLOT_FILE_NAME = f"plot{PLOT_FILE_TYPE}"


def plot_data(show_plot: bool = False) -> None:
    _use_plot_style()
    fig, _ = _make_fig_and_ax_objects()
    _show_plot(show_plot=show_plot)
    _save_plot(fig)


def _use_plot_style() -> None:
    logger.info("Using plot style %s", PATH_TO_STYLES)
    plt.style.use(PATH_TO_STYLES)


def _make_fig_and_ax_objects() -> Tuple[Figure, Axes]:
    logger.info("Plotting results")
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 4, 5, 6]
    fig, ax = plt.subplots()
    ax.plot(x, y)
    return fig, ax


def _show_plot(show_plot: bool = False) -> None:
    if show_plot:
        logger.info("Showing plot object")
        plt.show()


def _save_plot(
    fig: Figure, graph_file_name: str = PLOT_FILE_NAME, graphs_path: Path = PLOTS_PATH
) -> None:
    logger.info("Saving plot to %s", graphs_path / graph_file_name)
    make_dir_if_not_exist(graphs_path)
    fig.savefig(graphs_path / graph_file_name)
    plt.close(fig)

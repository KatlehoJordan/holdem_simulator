from pathlib import Path
from typing import Tuple

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from src.config import logger
from src.make_dir_if_does_not_exist import make_dir_if_not_exist

STYLES_PATH = Path("styles")
STYLES_FILE = "dgl_stylesheet.mpltstyle"
PATH_TO_STYLES = STYLES_PATH / STYLES_FILE
GRAPHS_PATH = Path("graphs")
GRAPH_FILE_TYPE = ".svg"
GRAPH_FILE_NAME = f"graph{GRAPH_FILE_TYPE}"


def graph():
    _use_plot_style()
    fig, _ = _make_graph_objects()
    _show_graph_object()
    _save_graph_object(fig)


def _use_plot_style() -> None:
    logger.info("Using plot style %s", PATH_TO_STYLES)
    plt.style.use(PATH_TO_STYLES)


def _make_graph_objects() -> Tuple[Figure, Axes]:
    logger.info("Graphing results")
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 4, 5, 6]
    fig, ax = plt.subplots()
    ax.plot(x, y)
    return fig, ax


def _show_graph_object() -> None:
    logger.info("Showing graph object")
    plt.show()


def _save_graph_object(
    fig: Figure, graph_file_name: str = GRAPH_FILE_NAME, graphs_path: Path = GRAPHS_PATH
) -> None:
    logger.info("Saving graph object to %s", graphs_path / graph_file_name)
    make_dir_if_not_exist(graphs_path)
    fig.savefig(graphs_path / graph_file_name)
    plt.close(fig)

from pathlib import Path
from typing import Union

import plotly.graph_objects as go
from pandas import DataFrame
from plotly.subplots import make_subplots

from src.aggregate_simulations import (
    APPEARANCES_STRING,
    HOLE_CARDS_FLAVOR_STRING,
    WIN_RATIO_ROUNDED_DOWN_STRING,
)
from src.config import PLOT_FILE_NAME, PLOTS_PATH, logger
from src.make_dir_if_does_not_exist import make_dir_if_not_exist


# TODO: Make the plots prettier by:
# Removing the grid lines
# Using monospace for labels and ticks
# Using gray for the chart borders, ticks, and labels
# using viridis magma for coloring of traces
def use_plotly(n_cols_to_show, show_plot, save_plot, wins_by_hole_cards_flavor_df):
    fig = _make_plotly_fig_and_ax_objects(
        wins_by_hole_cards_flavor_df, n_cols_to_show=n_cols_to_show
    )
    _show_plotly_plot(fig, show_plot=show_plot)
    _save_plotly_plot(fig, save_plot=save_plot)


def _make_plotly_fig_and_ax_objects(
    dataframe: DataFrame,
    n_cols_to_show: Union[int, None] = None,
    hole_cards_flavor_string: str = HOLE_CARDS_FLAVOR_STRING,
    win_ratio_rounded_down_string: str = WIN_RATIO_ROUNDED_DOWN_STRING,
    appearances_string: str = APPEARANCES_STRING,
) -> go.Figure:
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

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=x, y=y1), secondary_y=False)
    fig.add_trace(go.Scatter(x=x, y=y2, mode="lines"), secondary_y=True)
    fig.update_yaxes(range=[0, 1], secondary_y=False)
    fig.update_yaxes(range=[0, y2.max() * 1.1], secondary_y=True)

    return fig


def _show_plotly_plot(fig: go.Figure, show_plot: bool = False) -> None:
    if not show_plot:
        logger.info("Not showing plot object - pass show_plot=True to show it.")
        return
    logger.info("Showing plot object")
    fig.show()


def _save_plotly_plot(
    fig: go.Figure,
    save_plot: bool = False,
    graph_file_name: str = PLOT_FILE_NAME,
    graphs_path: Path = PLOTS_PATH,
) -> None:
    if not save_plot:
        logger.info("Not saving plot - pass save_plot=True to save it.")
        return
    logger.info("Saving plot to %s", graphs_path / graph_file_name)
    make_dir_if_not_exist(graphs_path)
    fig.write_image(str(graphs_path / graph_file_name))

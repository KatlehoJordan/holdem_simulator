from pathlib import Path
from typing import Union

import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame

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
def use_plotly(
    n_players_to_plot: int,
    n_cols_to_show: int,
    show_plot: bool,
    save_plot: bool,
    wins_by_hole_cards_flavor_df: DataFrame,
):
    fig = _make_plotly_fig_and_ax_objects(
        dataframe=wins_by_hole_cards_flavor_df,
        n_players_to_plot=n_players_to_plot,
        n_cols_to_show=n_cols_to_show,
    )
    _show_plotly_plot(fig, show_plot=show_plot)
    _save_plotly_plot(fig, save_plot=save_plot)


def _make_plotly_fig_and_ax_objects(
    dataframe: DataFrame,
    n_players_to_plot: int,
    n_cols_to_show: Union[int, None] = None,
    hole_cards_flavor_string: str = HOLE_CARDS_FLAVOR_STRING,
    win_ratio_rounded_down_string: str = WIN_RATIO_ROUNDED_DOWN_STRING,
    appearances_string: str = APPEARANCES_STRING,
) -> go.Figure:
    logger.info("Making plotly figure and axis objects")
    title = f"Win Ratio Rounded Down by {hole_cards_flavor_string} and {appearances_string} for {n_players_to_plot} Players"
    x_var = hole_cards_flavor_string
    y1_var = win_ratio_rounded_down_string
    y2_var = appearances_string
    logger.info("Sorting data frame descending by %s", y1_var)
    dataframe = dataframe.sort_values(by=y1_var, ascending=False)
    if n_cols_to_show is not None:
        dataframe = dataframe.head(n_cols_to_show)
    x = dataframe[x_var]
    y1 = dataframe[y1_var]
    y2 = dataframe[y2_var]

    fig = px.bar(dataframe, x=x, y=y1, color=y2, color_continuous_scale="Magma_r")

    fig.update_yaxes(showgrid=False, range=[0, 1], showticklabels=False)
    fig.update_layout(
        plot_bgcolor="white",
        title=title,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="center",
            x=0.5,
        ),
    )
    _mark_winners_losers_threshold(n_players_to_plot, fig)

    return fig


def _mark_winners_losers_threshold(n_players_to_plot, fig) -> None:
    winners_color = "limegreen"
    winners_line_height = 1 - (1 / n_players_to_plot) - 0.005
    losers_color = "red"
    _add_threshold_line(fig, winners_color, winners_line_height)
    _add_winner_loser_rectangle(fig, winners_line_height, 1, winners_color)
    _add_winner_loser_rectangle(fig, 0, winners_line_height, losers_color)
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="lines",
            line=dict(color=winners_color, width=1),
            name="Likely winners/losers threshold",  # The label
            showlegend=True,
        )
    )


def _add_threshold_line(fig, winners_color, winners_line_height):
    fig.add_shape(
        type="line",
        x0=0,
        y0=winners_line_height,
        x1=1,
        y1=winners_line_height,
        xref="paper",
        yref="y",
        line=dict(
            color=winners_color,
            width=1,
        ),
    )


def _add_winner_loser_rectangle(fig, y0, y1, color):
    fig.add_shape(
        type="rect",
        x0=0,
        y0=y0,
        x1=1,
        y1=y1,
        xref="paper",
        yref="y",
        fillcolor=color,
        opacity=0.1,
        line_width=0,
        layer="below",
    )


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

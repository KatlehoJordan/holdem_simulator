from pathlib import Path
from typing import Union

import plotly.express as px
import plotly.graph_objects as go
from matplotlib import colorbar
from pandas import DataFrame

from src.aggregate_simulations import (
    APPEARANCES_STRING,
    HOLE_CARDS_FLAVOR_STRING,
    WIN_RATIO_ROUNDED_DOWN_STRING,
    WIN_RATIO_STRING,
)
from src.config import (
    N_PLAYERS_STRING,
    N_POSSIBLE_PLAYERS,
    PLOT_FILE_NAME,
    PLOTS_PATH,
    logger,
)
from src.make_dir_if_does_not_exist import make_dir_if_not_exist

MINOR_FONT_SIZE = 12
MAJOR_FONT_SIZE = MINOR_FONT_SIZE + 2
TITLE_FONT_SIZE = MAJOR_FONT_SIZE + 6
PLOT_ALL_PLAYERS_STRING = "All"
ACCEPTABLE_N_PLAYERS_TO_PLOT = N_POSSIBLE_PLAYERS + [PLOT_ALL_PLAYERS_STRING]


# TODO: Ensure can export/save plotly plots
# TODO: Find a way to do grouped bar charts so can get multiple players on the same chart
def use_plotly(
    n_players_to_plot: Union[int, str],
    show_plot: bool,
    save_plot: bool,
    wins_by_hole_cards_flavor_df: DataFrame,
):
    fig = _make_plotly_fig_and_ax_objects(
        dataframe=wins_by_hole_cards_flavor_df,
        n_players_to_plot=n_players_to_plot,
    )
    _show_plotly_plot(fig, show_plot=show_plot)
    _save_plotly_plot(fig, save_plot=save_plot)


def _make_plotly_fig_and_ax_objects(
    dataframe: DataFrame,
    n_players_to_plot: Union[int, str],
) -> go.Figure:
    logger.info("Making plotly figure and axis objects")
    dataframe, x1, x2, y1, y2, y3 = _prepare_df_and_vars(dataframe, n_players_to_plot)

    # TODO: Implement x2 here (n_players) since currently not used
    fig = px.bar(
        dataframe,
        x=x1,
        y=y1,
        color=y2,
        color_continuous_scale="Magma_r",
        hover_data={y1.name: ":.0%", y3.name: ":.2%"},
    )

    fig.update_yaxes(showgrid=False, range=[0, 1], showticklabels=False, title_text="")
    fig.update_xaxes(showgrid=False, title_text="")
    fig.update_layout(plot_bgcolor="white")
    _adjust_colorbar(fig)
    _add_title(n_players_to_plot, fig)
    _mark_winners_losers_threshold(n_players_to_plot, fig)

    return fig


def _adjust_colorbar(
    fig,
    minor_font_size: int = MINOR_FONT_SIZE,
    major_font_size: int = MAJOR_FONT_SIZE,
    appearances_string: str = APPEARANCES_STRING,
):
    colorbar_title = f"{appearances_string}".title()
    fig.update_layout(
        coloraxis_colorbar=dict(
            thickness=10,
            title=colorbar_title,
            title_font=dict(size=major_font_size, family="serif"),
            tickfont=dict(size=minor_font_size, family="monospace"),
        ),
    )


def _prepare_df_and_vars(
    dataframe,
    n_players_to_plot: Union[int, str],
    n_players_string: str = N_PLAYERS_STRING,
    hole_cards_flavor_string: str = HOLE_CARDS_FLAVOR_STRING,
    win_ratio_string: str = WIN_RATIO_STRING,
    win_ratio_rounded_down_string: str = WIN_RATIO_ROUNDED_DOWN_STRING,
    appearances_string: str = APPEARANCES_STRING,
    plot_all_players_string: str = PLOT_ALL_PLAYERS_STRING,
):
    x1_var = hole_cards_flavor_string
    x2_var = n_players_string
    y1_var = win_ratio_rounded_down_string
    y2_var = appearances_string
    y3_var = win_ratio_string
    if n_players_to_plot != plot_all_players_string:
        dataframe[x2_var] = n_players_to_plot
    dataframe = dataframe[[x1_var, x2_var, y1_var, y2_var, y3_var]]
    dataframe[y3_var] = dataframe[y3_var].round(4)
    logger.info("Sorting data frame descending by %s", y1_var)
    dataframe = dataframe.sort_values(by=[y3_var, y1_var], ascending=False)
    x1 = dataframe[x1_var]
    x2 = dataframe[x2_var]
    y1 = dataframe[y1_var]
    y2 = dataframe[y2_var]
    y3 = dataframe[y3_var]
    return dataframe, x1, x2, y1, y2, y3


def _add_title(
    n_players_to_plot: Union[int, str],
    fig,
    hole_cards_flavor_string: str = HOLE_CARDS_FLAVOR_STRING,
    title_font_size: int = TITLE_FONT_SIZE,
):
    title = f"Best {hole_cards_flavor_string}s for {str(n_players_to_plot)} Players"

    fig.update_layout(
        title=title, title_font_size=title_font_size, title_font_family="serif"
    )


def _mark_winners_losers_threshold(n_players_to_plot, fig) -> None:
    winners_color = "limegreen"
    if type(n_players_to_plot) == int:
        winners_line_height = 1 - (1 / n_players_to_plot) - 0.005
        losers_color = "red"
        _add_threshold_line(fig, losers_color, winners_line_height)
        _add_winner_loser_rectangle(fig, winners_line_height, 1, winners_color)
        _add_winner_loser_rectangle(fig, 0, winners_line_height, losers_color)


def _add_threshold_line(
    fig, losers_color, winners_line_height, minor_font_size: int = MINOR_FONT_SIZE
):
    fig.add_shape(
        type="line",
        x0=0,
        y0=winners_line_height,
        x1=1,
        y1=winners_line_height,
        xref="paper",
        yref="y",
        line=dict(
            color=losers_color,
            width=1,
        ),
    )
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="lines",
            line=dict(color=losers_color, width=1),
            name="Likely Win/Lose Threshold",
            showlegend=True,
        )
    )
    fig.update_layout(
        legend=dict(
            font=dict(size=minor_font_size, family="serif"),
            yanchor="top",
            y=0.99,
            xanchor="center",
            x=0.5,
        )
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

import importlib
from typing import Union

import src.plot_builders_plotly
from src.config import N_PLAYERS_STRING, N_PLAYERS_TO_SIM_AGG_OR_PLOT
from src.get_wins_by_hole_cards_flavor_data import get_wins_by_hole_cards_flavor_df
from src.load_wins_by_hole_cards_flavor_df import load_wins_by_hole_cards_flavor_df
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
        df_to_plot = get_wins_by_hole_cards_flavor_df()
    else:
        wins_by_hole_cards_flavor_df = load_wins_by_hole_cards_flavor_df(
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

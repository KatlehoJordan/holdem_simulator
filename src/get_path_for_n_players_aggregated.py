from pathlib import Path

from src.config import (
    N_PLAYERS_PATH_PREFIX,
    N_PLAYERS_TO_SIM_AGG_OR_PLOT,
    PATH_TO_SIMULATIONS,
)


def get_path_for_n_players_aggregated(
    n_players_simulated_to_aggregate: int = N_PLAYERS_TO_SIM_AGG_OR_PLOT,
    path_to_simulations: Path = PATH_TO_SIMULATIONS,
    n_players_path_prefix: str = N_PLAYERS_PATH_PREFIX,
) -> Path:
    base_path_for_n_players = Path(
        f"{n_players_path_prefix}{n_players_simulated_to_aggregate}"
    )
    path_for_n_players = path_to_simulations / base_path_for_n_players
    return path_for_n_players

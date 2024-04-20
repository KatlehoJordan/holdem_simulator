from src.aggregate_simulations import aggregate_simulations
from src.config import (
    N_PLAYERS_TO_SIM_AGG_OR_PLOT,
    N_SIMS_FOR_2_PLAYERS_TO_KEEP_UNDER_50_MB,
    logger,
)
from src.simulate_hands import simulate_hands


# TODO: increase n_simulations sufficiently to get below thresholds specified in aggregate_simulations warnings.
# TODO: Run simulations for all player counts between 2 and 10.
def simulate_and_aggregate(
    n_sims_for_2_players_to_keep_under_50_mb: int = N_SIMS_FOR_2_PLAYERS_TO_KEEP_UNDER_50_MB,
    n_players_per_simulation: int = N_PLAYERS_TO_SIM_AGG_OR_PLOT,
) -> None:
    logger.setLevel("SIMULATING")
    n_simulations = int(
        2 * n_sims_for_2_players_to_keep_under_50_mb / n_players_per_simulation
    )
    simulate_hands(
        n_simulations=n_simulations,
        n_players_per_simulation=n_players_per_simulation,
    )
    aggregate_simulations(n_players_to_sim_or_aggregate=n_players_per_simulation)

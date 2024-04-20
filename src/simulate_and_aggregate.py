from src.aggregate_simulations import aggregate_simulations
from src.config import N_PLAYERS_TO_SIM_AGG_OR_PLOT, N_SIMS, logger
from src.simulate_hands import simulate_hands


# TODO: increase n_simulations sufficiently to get below thresholds specified in aggregate_simulations. May want to disable logging to make simulations faster.
# TODO: Run simulations for all player counts between 2 and 10.
def simulate_and_aggregate(
    n_simulations: int = N_SIMS,
    n_players_per_simulation: int = N_PLAYERS_TO_SIM_AGG_OR_PLOT,
) -> None:
    logger.setLevel("SIMULATING")
    simulate_hands(
        n_simulations=n_simulations,
        n_players_per_simulation=n_players_per_simulation,
    )
    aggregate_simulations()
    exit()

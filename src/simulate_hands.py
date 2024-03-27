from src.config import logger
from src.hand import Hand
from src.players_ahead_of_you import PlayersAheadOfYou

N_SIMULATIONS = 2
N_PLAYERS_PER_SIMULATION = 2


def simulate_hands(
    n_simulations: int = N_SIMULATIONS,
    n_players_per_simulation: int = N_PLAYERS_PER_SIMULATION,
) -> None:
    logger.info("Simulating %s hands", n_simulations)
    for _ in range(n_simulations):
        console_iteration_visualizer = "-" * 80
        logger.info(console_iteration_visualizer)
        iter = _ + 1
        logger.info("Iteration: %s", iter)
        logger.info(console_iteration_visualizer)
        logger.info("Simulating %s players", n_players_per_simulation)
        _ = Hand(n_players_ahead_of_you=PlayersAheadOfYou(n_players_per_simulation - 1))

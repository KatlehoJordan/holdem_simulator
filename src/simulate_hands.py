from pathlib import Path

import pandas as pd

from src.card import VALID_CARDS_DICT
from src.config import logger
from src.hand import Hand
from src.players_ahead_of_you import PlayersAheadOfYou

N_SIMULATIONS = 1
N_PLAYERS_PER_SIMULATION = 2
PATH_TO_SIMULATIONS = Path("simulations")


def simulate_hands(
    n_simulations: int = N_SIMULATIONS,
    n_players_per_simulation: int = N_PLAYERS_PER_SIMULATION,
) -> None:
    logger.info("Simulating %s hands", n_simulations)
    for simulation in range(n_simulations):
        console_iteration_visualizer = "-" * 80
        logger.info(console_iteration_visualizer)
        iter = simulation + 1
        logger.info("Iteration: %s", iter)
        logger.info(console_iteration_visualizer)
        logger.info("Simulating %s players", n_players_per_simulation)
        hand = Hand(
            n_players_ahead_of_you=PlayersAheadOfYou(n_players_per_simulation - 1)
        )
        df = _extract_results_data(hand, n_players_per_simulation)

        print("Pause here")

        # TODO: Add logic to this function to cycle over the compare_player_hands function to determine the winner and or ties, saving an attribute for the best_hand and the 'hole_cards_flavor'.
        # TODO: Extract result in terms of winning or tying hands, losing hands, and number of players for later tabulating during simulation of 1000s of hands
        # TODO: Measure how frequently each player wins, ties, or loses (should expect uniform distribution for each player if my random drawing is working correctly)
        # TODO: Measure how frequently each card appears in a hand (should expect a uniform distribution if my random drawing is working correctly)


def _extract_results_data(
    hand: Hand, n_players_per_simulation: int = N_PLAYERS_PER_SIMULATION
):
    logger.info("Extracting info from hand")
    data = {
        "n_players": n_players_per_simulation,
        "winning_type": hand.winning_type,
        "n_winners": len(hand.winning_hands),
        "winning_hands": hand.winning_hands,
        "community_cards": hand.player_hands_in_the_hand[0].community_cards,
        "your_hand": hand.player_hands_in_the_hand[0],
    }
    for player in range(n_players_per_simulation):
        hand_key = f"player_{player}s_hand" if player != 0 else "your_hand"
        data[hand_key] = hand.player_hands_in_the_hand[player]

        hole_cards_key = (
            f"player_{player}s_hole_cards" if player != 0 else "your_hole_cards"
        )
        data[hole_cards_key] = hand.player_hands_in_the_hand[player].hole_cards

        win_key = f"player_{player}_wins" if player != 0 else "you_win"
        data[win_key] = data[hand_key] in data["winning_hands"]

        win_as_float_key = (
            f"player_{player}_wins_as_float" if player != 0 else "you_win_as_float"
        )
        data[win_as_float_key] = (1.0 / data["n_winners"]) if data[win_key] else 0.0

        # TODO: Add columns for all unique_cards and indicate with True or False if they appear in the hand
        # TODO: After the previous, make a summary in order to get %age win for each player, and %age of each unique_card in order to validate your random drawing is working as expected
        # TODO: Add columns for all hole_cards_flavors and indicate with True or False if they appear in the hand
        # TODO: After previous, calculate %age of each hole_cards_flavor

    df = pd.DataFrame([data])
    return df


# TODO: Finish building this function
def make_simulations_results_file(
    path_to_simulations: Path = PATH_TO_SIMULATIONS,
    n_players_per_simulation: int = N_PLAYERS_PER_SIMULATION,
):
    logger.info("Making simulations results file")
    if not path_to_simulations.exists():
        path_to_simulations.mkdir()
    path_to_simulations_results = (
        path_to_simulations / f"data for {n_players_per_simulation} players.csv"
    )
    # TODO: Once satisfied with the structure of the data output, modify this to instead append to the file if it already exists
    if path_to_simulations_results.exists():
        logger.info("Removing old simulations results file")
        path_to_simulations_results.unlink()
    logger.info("Creating new simulations results file")
    with open(path_to_simulations_results, "w") as f:
        f.write("hand_number,player_number,hand_flavor\n")
    logger.info("Simulations results file created")

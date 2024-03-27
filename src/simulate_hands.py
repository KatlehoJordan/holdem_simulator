from pathlib import Path

import pandas as pd

from src.card import VALID_CARDS_DICT
from src.community_cards import N_CARDS_IN_COMMUNITY_CARDS
from src.config import logger
from src.hand import Hand
from src.hole_cards import N_HOLE_CARDS_PER_PLAYER
from src.players_ahead_of_you import PlayersAheadOfYou

# TODO: increase n_simulations to at least 10000 for 10 players. May want to disable logging to make it faster.
# TODO: Run simulations for all player counts between 2 and 10.
N_SIMULATIONS = 1
N_PLAYERS_PER_SIMULATION = 2
PATH_TO_SIMULATIONS = Path("simulations")
TOLERANCE_THRESHOLD_FOR_RANDOM_DRAWING = 0.1


def simulate_hands(
    n_simulations: int = N_SIMULATIONS,
    n_players_per_simulation: int = N_PLAYERS_PER_SIMULATION,
) -> None:
    logger.info("Initializing empty dataframe")
    df = pd.DataFrame()
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
        simulated_data = _extract_results_data(hand, n_players_per_simulation)
        df = pd.concat([df, simulated_data], ignore_index=True)
        # TODO: Add logic to save the simulated_data to a csv file

    aggregated_wins_df = _aggregate_total_wins(
        df,
        n_simulations,
        n_players_per_simulation,
    )
    # TODO: Add logic to save the aggregated_df to a csv file and visualize the results

    # TODO: Add logic to create, validate, save, and visualize an aggregated dataframe for totalling how often different cards appear in the hand, similar to what you've done with _aggregate_total_wins for wins
    print("Pause here")


def _aggregate_total_wins(
    df: pd.DataFrame,
    n_simulations: int = N_SIMULATIONS,
    n_players_per_simulation: int = N_PLAYERS_PER_SIMULATION,
    tolerance_threshold_for_random_drawing: float = TOLERANCE_THRESHOLD_FOR_RANDOM_DRAWING,
) -> pd.DataFrame:
    total_wins = 0.0
    out_df = pd.DataFrame()
    for player in range(n_players_per_simulation):
        wins_as_float_key = (
            f"player_{player}_wins_as_float" if player != 0 else "you_win_as_float"
        )
        this_players_wins = sum(df[wins_as_float_key])
        expected_wins = n_simulations / n_players_per_simulation
        if (
            abs(this_players_wins - expected_wins)
            > tolerance_threshold_for_random_drawing * expected_wins
        ):
            if player == 0:
                player = "you"
            raise ValueError(
                f"Player {player}'s wins deviate from the expected number of wins by more than {tolerance_threshold_for_random_drawing:.0%}. A larger sample should be drawn or else the random assignment of cards to players is not working."
            )
        total_wins += this_players_wins
        out_df = pd.concat(
            [out_df, pd.DataFrame([{"player": player, "wins": this_players_wins}])],
            ignore_index=True,
        )

    if total_wins != n_simulations:
        raise ValueError("The sum of wins should equal the number of simulations")
    return out_df


def _extract_results_data(
    hand: Hand,
    n_players_per_simulation: int = N_PLAYERS_PER_SIMULATION,
    valid_cards_dict: dict = VALID_CARDS_DICT,
) -> pd.DataFrame:
    logger.info("Extracting info from hand")
    data = {
        "n_players": n_players_per_simulation,
        "all_cards_in_the_hand": hand.all_cards_in_the_hand,
        "winning_type": hand.winning_type,
        "n_winners": len(hand.winning_hands),
        "winning_hands": hand.winning_hands,
        "winning_hole_cards_flavors": hand.winning_hole_type_flavors,
        "community_cards": hand.player_hands_in_the_hand[0].community_cards,
        "your_hand": hand.player_hands_in_the_hand[0],
    }
    for player in range(n_players_per_simulation):
        hand_key = f"player_{player}s_hand" if player != 0 else "your_hand"
        data[hand_key] = hand.player_hands_in_the_hand[player]

        # TODO: Decide if should remove/deprecate the following block that is commented out
        # hole_cards_key = (
        #     f"player_{player}s_hole_cards" if player != 0 else "your_hole_cards"
        # )
        # data[hole_cards_key] = hand.player_hands_in_the_hand[player].hole_cards

        # hole_cards_flavor_key = (
        #     f"player_{player}s_hole_cards_flavor"
        #     if player != 0
        #     else "your_hole_cards_flavor"
        # )
        # data[hole_cards_flavor_key] = hand.player_hands_in_the_hand[
        #     player
        # ].hole_cards.hole_cards_flavor

        win_key = f"player_{player}_wins" if player != 0 else "you_win"
        data[win_key] = data[hand_key] in data["winning_hands"]

        win_as_float_key = (
            f"player_{player}_wins_as_float" if player != 0 else "you_win_as_float"
        )
        data[win_as_float_key] = (1.0 / data["n_winners"]) if data[win_key] else 0.0

    data["n_cards_in_hand"] = 0
    for card in valid_cards_dict.keys():
        card_key = valid_cards_dict[card].name
        data[card_key] = card_key in [
            card.name for card in data["all_cards_in_the_hand"]
        ]
        data["n_cards_in_hand"] += data[card_key]

    df = pd.DataFrame([data])

    _validate_n_cards_in_hand(
        df=df,
        n_players_per_simulation=n_players_per_simulation,
    )

    # TODO: Add columns for all unique_cards and indicate with True or False if they appear in the hand
    # TODO: After the previous, make a summary in order to get %age win for each player, and %age of each unique_card in order to validate your random drawing is working as expected
    # TODO: Add columns for all hole_cards_flavors and indicate with True or False if they appear in the hand
    # TODO: After previous, calculate %age of each hole_cards_flavor
    return df


def _validate_n_cards_in_hand(
    df: pd.DataFrame,
    n_players_per_simulation: int = N_PLAYERS_PER_SIMULATION,
    n_cards_in_community_cards: int = N_CARDS_IN_COMMUNITY_CARDS,
    n_hole_cards_per_player: int = N_HOLE_CARDS_PER_PLAYER,
) -> None:
    if not (
        df["n_cards_in_hand"]
        == (
            n_cards_in_community_cards
            + n_hole_cards_per_player * n_players_per_simulation
        )
    ).all():
        raise ValueError(
            f"n_cards_in_hand is not equal to ({n_cards_in_community_cards} + {n_hole_cards_per_player} * {n_players_per_simulation})"
        )


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


# TODO: Add logic to cycle over the compare_player_hands function to determine the winner and or ties, saving an attribute for the best_hand and the 'hole_cards_flavor'.
# TODO: Extract result in terms of winning or tying hands, losing hands, and number of players for later tabulating during simulation of 1000s of hands
# TODO: Measure how frequently each card appears in a hand (should expect a uniform distribution if my random drawing is working correctly)

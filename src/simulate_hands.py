import shutil
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
PATH_TO_SIMULATIONS_DATA_RESULTS = Path("simulations")
PATH_TO_AGGREGATED_DATA_RESULTS = PATH_TO_SIMULATIONS_DATA_RESULTS / "aggregated"
PATH_TO_UNAGGREGATED_DATA_RESULTS = PATH_TO_SIMULATIONS_DATA_RESULTS / "unaggregated"
NAME_OF_ARCHIVED_SIMULATIONS_FOLDER = "archived_simulations"
PATH_TO_ARCHIVED_SIMULATIONS_DATA_RESULTS = (
    PATH_TO_SIMULATIONS_DATA_RESULTS / NAME_OF_ARCHIVED_SIMULATIONS_FOLDER
)
TOLERANCE_THRESHOLD_FOR_RANDOM_DRAWING = 0.1


def simulate_hands(
    n_simulations: int = N_SIMULATIONS,
    n_players_per_simulation: int = N_PLAYERS_PER_SIMULATION,
) -> None:
    logger.info("Initializing empty dataframe")
    simulated_data_df = pd.DataFrame()
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
        # TODO: Modify _extract_results_data so that community cards are included as a single line in the dataframe instead of with new lines
        # TODO: Modify _extract_results_data so that when it is saved as .csv it does not have a mix of both "" and '' since this can cause problems later as evidenced by CSV linter.
        # TODO: Modify _extract_results_data to include True or False for each type of hole_cards_flavor
        simulated_data = _extract_results_data(hand, n_players_per_simulation)
        simulated_data_df = pd.concat(
            [simulated_data_df, simulated_data], ignore_index=True
        )

    _make_simulations_results_file(simulated_data_df)
    # TODO: Modify _aggregate_total_wins to use the file created by _make_simulations_results_file. It should output a dataframe with a single line of aggregated data instead of many lines. Then, add logic to save the aggregated_df to a csv file and visualize the results. Want to have controls that no obvious bias for any one player to win, and want to ensure that no obvious bias for any specific cards to be drawn.
    aggregated_wins_df = _aggregate_total_wins(
        simulated_data_df,
        n_simulations,
        n_players_per_simulation,
    )
    # TODO: Add logic to save the aggregated_df to a csv file. Current implementation is appending to the previous aggregated file, which is not the desired outcome, so many not be able to use the same function as for the raw simulation data as first thought.
    _make_simulations_results_file(aggregated_wins_df, aggregated_results=True)

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
        # if (
        #     abs(this_players_wins - expected_wins)
        #     > tolerance_threshold_for_random_drawing * expected_wins
        # ):
        #     if player == 0:
        #         player = "you"
        #     raise ValueError(
        #         f"Player {player}'s wins deviate from the expected number of wins by more than {tolerance_threshold_for_random_drawing:.0%}. A larger sample should be drawn or else the random assignment of cards to players is not working."
        #     )
        total_wins += this_players_wins
        out_df = pd.concat(
            [out_df, pd.DataFrame([{"player": player, "wins": this_players_wins}])],
            ignore_index=True,
        )

    # if total_wins != n_simulations:
    #     raise ValueError("The sum of wins should equal the number of simulations")
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


def _make_simulations_results_file(
    df: pd.DataFrame,
    aggregated_results: bool = False,
    path_to_aggregated_directory: Path = PATH_TO_AGGREGATED_DATA_RESULTS,
    path_to_unaggregated_directory: Path = PATH_TO_UNAGGREGATED_DATA_RESULTS,
    path_to_archive: Path = PATH_TO_ARCHIVED_SIMULATIONS_DATA_RESULTS,
    n_players_per_simulation: int = N_PLAYERS_PER_SIMULATION,
) -> None:
    _make_dir_if_not_exist(path_to_archive)
    _make_dir_if_not_exist(path_to_aggregated_directory)
    _make_dir_if_not_exist(path_to_unaggregated_directory)

    if aggregated_results:
        subfolder = path_to_aggregated_directory
        file_name_prefix = "aggregated"
    else:
        subfolder = path_to_unaggregated_directory
        file_name_prefix = "unaggregated"
    file_for_simulations_results = (
        subfolder
        / f"{file_name_prefix} data for {n_players_per_simulation} players.csv"
    )

    if file_for_simulations_results.exists():
        logger.info(
            "%s already exists. Copying it to the archive folder with a timestamp.",
            file_for_simulations_results,
        )
        timestamp = pd.Timestamp.now().strftime("%Y-%m-%d")
        shutil.copy2(
            file_for_simulations_results,
            path_to_archive
            / f"{file_for_simulations_results.stem} dated {timestamp}.csv",
        )

        logger.info("Appending new data to %s", file_for_simulations_results)
        df.to_csv(file_for_simulations_results, mode="a", header=False, index=False)
    else:
        logger.info("%s does not exist. Creating it now.", file_for_simulations_results)
        df.to_csv(file_for_simulations_results, index=False)


def _make_dir_if_not_exist(path_to_dir: Path) -> None:
    if not path_to_dir.exists():
        logger.info("%s directory does not exist. Making it now.", path_to_dir)
        path_to_dir.mkdir(parents=True)


# TODO: Add logic to cycle over the compare_player_hands function to determine the winner and or ties, saving an attribute for the best_hand and the 'hole_cards_flavor'.
# TODO: Extract result in terms of winning or tying hands, losing hands, and number of players for later tabulating during simulation of 1000s of hands
# TODO: Measure how frequently each card appears in a hand (should expect a uniform distribution if my random drawing is working correctly)

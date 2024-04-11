import math
import shutil
from pathlib import Path

import pandas as pd

from src.card import VALID_CARDS_DICT
from src.community_cards import N_CARDS_IN_COMMUNITY_CARDS
from src.config import (
    PATH_TO_ARCHIVED_SIMULATIONS_DATA_RESULTS,
    PATH_TO_SIMULATIONS_DATA_RESULTS,
    logger,
)
from src.hand import HAND_WINNER_FLAVOR, Hand
from src.hole_cards import N_HOLE_CARDS_PER_PLAYER, VALID_HOLE_CARDS_FLAVORS_LIST
from src.make_dir_if_does_not_exist import make_dir_if_not_exist
from src.players_ahead_of_you import PlayersAheadOfYou

N_SIMULATIONS = 1
N_PLAYERS_PER_SIMULATION = 2
PATH_TO_UNAGGREGATED_DATA_RESULTS = PATH_TO_SIMULATIONS_DATA_RESULTS / "unaggregated"
N_CARDS_IN_HAND_STRING = "n_cards_in_hand"
N_HOLE_CARDS_FLAVORS_IN_HAND_STRING = "n_hole_cards_flavors_in_hand"


def simulate_hands(
    n_simulations: int = N_SIMULATIONS,
    n_players_per_simulation: int = N_PLAYERS_PER_SIMULATION,
) -> Path:
    logger.info("Initializing empty dataframe")
    simulated_data_df = pd.DataFrame()
    logger.info("Simulating %s hands", n_simulations)
    for simulation in range(n_simulations):
        # TODO: Take away this warning when done with simulations
        logger.warn("Simulation number %s", simulation + 1)
        logger.info("Simulating %s players", n_players_per_simulation)
        hand = Hand(
            n_players_ahead_of_you=PlayersAheadOfYou(n_players_per_simulation - 1)
        )
        simulated_data = _extract_results_data(hand, n_players_per_simulation)
        simulated_data_df = pd.concat(
            [simulated_data_df, simulated_data], ignore_index=True
        )

    file_path_for_simulations_results = _make_simulations_results_file(
        simulated_data_df
    )
    return file_path_for_simulations_results


def _initialize_data_dictionary(
    hand: Hand, n_players_per_simulation: int = N_PLAYERS_PER_SIMULATION
) -> dict:
    logger.info("Initializing data dictionary")
    data = {
        "n_players": n_players_per_simulation,
        "all_cards_in_the_hand": [card.name for card in hand.all_cards_in_the_hand],
        "all_hole_cards_flavors_in_the_hand": [
            hole_cards_flavors
            for hole_cards_flavors in hand.losing_hole_cards_flavors
            + hand.winning_hole_cards_flavors
        ],
        "winning_type": hand.winning_type,
        "n_winners": len(hand.winning_hands),
        "winning_hands": hand.winning_hands[0].hand_type,
        "winning_hole_cards_flavors": hand.winning_hole_cards_flavors,
        "community_cards": [
            card.name for card in hand.player_hands_in_the_hand[0].community_cards.cards
        ],
    }

    return data


def _add_player_specific_data(
    hand: Hand,
    data_dict: dict,
    n_players_per_simulation: int = N_PLAYERS_PER_SIMULATION,
    single_winner_hand_winner_flavor: str = HAND_WINNER_FLAVOR,
) -> dict:
    logger.info("Adding player-specific data to dictionary")
    sum_of_wins_as_float = 0.0
    count_winners = 0
    for player in range(n_players_per_simulation):
        hand_type_key = (
            f"player_{player}s_hand_type" if player != 0 else "your_hand_type"
        )
        data_dict[hand_type_key] = hand.player_hands_in_the_hand[player]

        hole_cards_key = (
            f"player_{player}s_hole_cards" if player != 0 else "your_hole_cards"
        )
        data_dict[hole_cards_key] = (
            hand.player_hands_in_the_hand[player].hole_cards.hi_card.name
            + ", "
            + hand.player_hands_in_the_hand[player].hole_cards.lo_card.name
        )

        hole_cards_flavor_key = (
            f"player_{player}s_hole_cards_flavor"
            if player != 0
            else "your_hole_cards_flavor"
        )
        data_dict[hole_cards_flavor_key] = hand.player_hands_in_the_hand[
            player
        ].hole_cards.hole_cards_flavor

        win_key = f"player_{player}_wins" if player != 0 else "you_win"
        data_dict[win_key] = (
            data_dict[hand_type_key].hand_type.name == data_dict["winning_hands"].name
        )

        win_as_float_key = (
            f"player_{player}_wins_as_float" if player != 0 else "you_win_as_float"
        )
        data_dict[win_as_float_key] = (
            (1.0 / data_dict["n_winners"]) if data_dict[win_key] else 0.0
        )
        sum_of_wins_as_float += data_dict[win_as_float_key]
        if data_dict[win_key]:
            count_winners += 1
    if not math.isclose(sum_of_wins_as_float, 1.0, rel_tol=1e-9):
        raise ValueError(
            f"Sum of wins as float is not close to 1.0, indicating some wins are being tallied incorrectly: {sum_of_wins_as_float}"
        )
    if hand.winning_type == single_winner_hand_winner_flavor and count_winners != 1:
        raise ValueError(
            f"Winning type is {single_winner_hand_winner_flavor}, but count_winners is not 1: {count_winners}, indicating some wins are being tallied incorrectly!"
        )

    return data_dict


def _indicate_which_cards_appear_in_hand(
    data: dict,
    valid_cards_dict: dict = VALID_CARDS_DICT,
    n_cards_in_hand_string: str = N_CARDS_IN_HAND_STRING,
) -> pd.DataFrame:
    data[n_cards_in_hand_string] = 0
    for card in valid_cards_dict.keys():
        card_key = valid_cards_dict[card].name
        data[card_key] = int(card_key in data["all_cards_in_the_hand"])
        data[n_cards_in_hand_string] += data[card_key]

    df = pd.DataFrame([data])
    return df


def _validate_n_cards_in_hand(
    df: pd.DataFrame,
    n_players_per_simulation: int = N_PLAYERS_PER_SIMULATION,
    n_cards_in_community_cards: int = N_CARDS_IN_COMMUNITY_CARDS,
    n_hole_cards_per_player: int = N_HOLE_CARDS_PER_PLAYER,
    n_cards_in_hand_string: str = N_CARDS_IN_HAND_STRING,
) -> None:
    if not (
        df[n_cards_in_hand_string]
        == (
            n_cards_in_community_cards
            + n_hole_cards_per_player * n_players_per_simulation
        )
    ).all():
        raise ValueError(
            f"n_cards_in_hand is not equal to ({n_cards_in_community_cards} + {n_hole_cards_per_player} * {n_players_per_simulation})"
        )


def _indicate_which_hole_cards_flavors_appear_in_hand(
    data_frame: pd.DataFrame,
    valid_hole_cards_flavors_list: list = VALID_HOLE_CARDS_FLAVORS_LIST,
    n_hole_cards_flavors_in_hand_string: str = N_HOLE_CARDS_FLAVORS_IN_HAND_STRING,
) -> pd.DataFrame:
    data_frame[n_hole_cards_flavors_in_hand_string] = 0
    new_data = {}
    for hole_cards_flavor in valid_hole_cards_flavors_list:
        hole_cards_flavor_key = hole_cards_flavor
        if hole_cards_flavor_key not in new_data:
            new_data[hole_cards_flavor_key] = 0
        # new_data[hole_cards_flavor_key] += (
        #     hole_cards_flavor in data_frame["all_hole_cards_flavors_in_the_hand"][0]
        new_data[hole_cards_flavor_key] += data_frame[
            "all_hole_cards_flavors_in_the_hand"
        ][0].count(hole_cards_flavor)
        data_frame[n_hole_cards_flavors_in_hand_string] += new_data[
            hole_cards_flavor_key
        ]

    new_df = pd.DataFrame(new_data, index=data_frame.index)
    data_frame = pd.concat([data_frame, new_df], axis=1)
    return data_frame


def _validate_hole_cards_flavors_tagged(
    df: pd.DataFrame,
    n_players_per_simulation: int = N_PLAYERS_PER_SIMULATION,
    n_hole_cards_flavors_in_hand_string: str = N_HOLE_CARDS_FLAVORS_IN_HAND_STRING,
) -> None:
    if not (
        df[n_hole_cards_flavors_in_hand_string] == (n_players_per_simulation)
    ).all():
        raise ValueError(
            f"{n_hole_cards_flavors_in_hand_string} is not equal to {n_players_per_simulation}, indicating not all hole_cards_flavors are being counted correctly!"
        )


def _extract_results_data(
    hand: Hand,
    n_players_per_simulation: int = N_PLAYERS_PER_SIMULATION,
) -> pd.DataFrame:
    logger.info("Extracting info from hand")
    data_dict = _initialize_data_dictionary(
        hand=hand, n_players_per_simulation=n_players_per_simulation
    )
    data_dict = _add_player_specific_data(
        hand=hand,
        data_dict=data_dict,
        n_players_per_simulation=n_players_per_simulation,
    )
    data_frame = _indicate_which_cards_appear_in_hand(data_dict)
    _validate_n_cards_in_hand(
        df=data_frame,
        n_players_per_simulation=n_players_per_simulation,
    )

    data_frame = _indicate_which_hole_cards_flavors_appear_in_hand(data_frame)
    _validate_hole_cards_flavors_tagged(
        df=data_frame,
        n_players_per_simulation=n_players_per_simulation,
    )
    return data_frame


def _make_simulations_results_file(
    df: pd.DataFrame,
    path_to_archive: Path = PATH_TO_ARCHIVED_SIMULATIONS_DATA_RESULTS,
) -> Path:
    file_path_for_simulations_results = make_file_path_for_unaggregated_simulations()

    if file_path_for_simulations_results.exists():
        logger.info(
            "%s already exists. Copying it to the archive folder with a timestamp.",
            file_path_for_simulations_results,
        )
        timestamp = pd.Timestamp.now().strftime("%Y-%m-%d")
        shutil.copy2(
            file_path_for_simulations_results,
            path_to_archive
            / f"{file_path_for_simulations_results.stem} dated {timestamp}.csv",
        )

        logger.info("Appending new data to %s", file_path_for_simulations_results)
        df.to_csv(
            file_path_for_simulations_results, mode="a", header=False, index=False
        )
    else:
        logger.info(
            "%s does not exist. Creating it now.", file_path_for_simulations_results
        )
        df.to_csv(file_path_for_simulations_results, index=False)
    return file_path_for_simulations_results


def make_file_path_for_unaggregated_simulations(
    path_to_unaggregated_directory: Path = PATH_TO_UNAGGREGATED_DATA_RESULTS,
    path_to_archive: Path = PATH_TO_ARCHIVED_SIMULATIONS_DATA_RESULTS,
    n_players_per_simulation: int = N_PLAYERS_PER_SIMULATION,
) -> Path:
    make_dir_if_not_exist(path_to_archive)
    make_dir_if_not_exist(path_to_unaggregated_directory)

    subfolder = path_to_unaggregated_directory
    file_name_prefix = "unaggregated"
    file_for_simulations_results = (
        subfolder
        / f"{file_name_prefix} data for {n_players_per_simulation} players.csv"
    )

    return file_for_simulations_results

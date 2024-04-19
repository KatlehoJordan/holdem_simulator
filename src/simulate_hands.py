import math
import re
import shutil
from pathlib import Path

import pandas as pd

from src.card import VALID_CARDS_DICT
from src.community_cards import N_CARDS_IN_COMMUNITY_CARDS
from src.config import (
    FILE_SAVE_TYPE,
    N_PLAYERS_PATH_PREFIX,
    N_PLAYERS_TO_SIM_OR_AGGREGATE,
    PATH_TO_ARCHIVED_SIMULATIONS,
    PATH_TO_SIMULATIONS,
    logger,
)
from src.hand import HAND_WINNER_FLAVOR, Hand
from src.hole_cards import N_HOLE_CARDS_PER_PLAYER, VALID_HOLE_CARDS_FLAVORS_LIST
from src.make_dir_if_does_not_exist import make_dir_if_not_exist
from src.players_ahead_of_you import PlayersAheadOfYou

N_SIMULATIONS = 1
PATH_TO_UNAGGREGATED_DATA = Path("unaggregated")
N_CARDS_IN_HAND_STRING = "n_cards_in_hand"
N_HOLE_CARDS_FLAVORS_IN_HAND_STRING = "n_hole_cards_flavors_in_hand"
FILE_SUFFIX_NUMBER = 1


def simulate_hands(
    n_simulations: int = N_SIMULATIONS,
    n_players_per_simulation: int = N_PLAYERS_TO_SIM_OR_AGGREGATE,
) -> Path:
    if n_simulations > 50_000:
        raise ValueError(
            "n_simulations cannot be over 50,000 or else the file sizes will get too large and GitHub may stop accepting pushes."
        )
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
        simulated_data_df, n_players_per_simulation=n_players_per_simulation
    )
    return file_path_for_simulations_results


def _initialize_data_dictionary(
    hand: Hand,
    n_players_per_simulation: int,
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
    n_players_per_simulation: int,
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
    # TODO: Remove this next bit of code after done troubleshooting since it is redundant with the next function and is only here for troubleshooting.
    if not math.isclose(sum_of_wins_as_float, 1.0, rel_tol=1e-9):
        raise ValueError(
            f"Sum of wins as float is {sum_of_wins_as_float}, which is not close to 1.0, indicating some wins are being tallied incorrectly!"
        )
    _validate_player_specific_data(hand, sum_of_wins_as_float, count_winners)

    return data_dict


def _validate_player_specific_data(
    hand: Hand,
    sum_of_wins_as_float: float,
    count_winners: int,
    single_winner_hand_winner_flavor: str = HAND_WINNER_FLAVOR,
) -> None:
    logger.info("Validating player-specific data")
    if not math.isclose(sum_of_wins_as_float, 1.0, rel_tol=1e-9):
        raise ValueError(
            f"Sum of wins as float is {sum_of_wins_as_float}, which is not close to 1.0, indicating some wins are being tallied incorrectly!"
        )
    if hand.winning_type == single_winner_hand_winner_flavor and count_winners != 1:
        raise ValueError(
            f"Winning type is {single_winner_hand_winner_flavor}, but count_winners is not 1: {count_winners}, indicating some wins are being tallied incorrectly!"
        )


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
    n_players_per_simulation: int,
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
    n_players_per_simulation: int,
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
    n_players_per_simulation: int,
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


# TODO: Refactor or simplify this function
def _make_simulations_results_file(
    df: pd.DataFrame,
    n_players_per_simulation: int,
    path_to_archive: Path = PATH_TO_ARCHIVED_SIMULATIONS,
    path_to_simulations: Path = PATH_TO_SIMULATIONS,
    file_save_type: str = FILE_SAVE_TYPE,
    file_suffix_number: int = FILE_SUFFIX_NUMBER,
    n_players_path_prefix: str = N_PLAYERS_PATH_PREFIX,
    path_to_unaggregated: Path = PATH_TO_UNAGGREGATED_DATA,
) -> Path:
    file_path_for_simulations_results = _make_file_path_for_unaggregated_simulations(
        file_suffix_number=file_suffix_number,
        n_players_per_simulation=n_players_per_simulation,
    )

    if file_path_for_simulations_results.exists():
        logger.info(
            "%s already exists. Copying it to the archive folder with a timestamp.",
            file_path_for_simulations_results,
        )
        timestamp = pd.Timestamp.now().strftime("%Y-%m-%d")
        base_path_for_n_players = Path(
            f"{n_players_path_prefix}{n_players_per_simulation}"
        )
        backup_file_path = (
            path_to_simulations
            / base_path_for_n_players
            / path_to_archive
            / path_to_unaggregated
        )
        make_dir_if_not_exist(backup_file_path)
        backup_file = (
            backup_file_path
            / f"{file_path_for_simulations_results.stem}{file_save_type}"
        )
        shutil.copy2(
            file_path_for_simulations_results,
            backup_file,
        )
        match = re.search(r"\d{3}", file_path_for_simulations_results.name)
        if match:
            ddd = int(match.group())
            logger.info("Extracted <ddd> from file name: %d", ddd)
            logger.info("Incrementing <ddd> by 1.")
            file_path_for_simulations_results = _make_simulations_results_file(
                df=df,
                n_players_per_simulation=n_players_per_simulation,
                file_suffix_number=ddd + 1,
            )
        else:
            raise ValueError("Could not extract <ddd> from file name.")
    else:
        logger.info(
            "%s does not exist. Creating it now.", file_path_for_simulations_results
        )
        df.to_csv(file_path_for_simulations_results, index=False)
    return file_path_for_simulations_results


def _make_file_path_for_unaggregated_simulations(
    n_players_per_simulation: int,
    file_suffix_number: int = FILE_SUFFIX_NUMBER,
    path_to_simulations: Path = PATH_TO_SIMULATIONS,
    path_to_unaggregated_directory: Path = PATH_TO_UNAGGREGATED_DATA,
    path_to_archive: Path = PATH_TO_ARCHIVED_SIMULATIONS,
    file_save_type: str = FILE_SAVE_TYPE,
    n_players_path_prefix: str = N_PLAYERS_PATH_PREFIX,
) -> Path:
    base_path_for_n_players = Path(f"{n_players_path_prefix}{n_players_per_simulation}")
    make_dir_if_not_exist(
        path_to_simulations / base_path_for_n_players / path_to_archive
    )
    _ = make_folder_for_unaggregated_simulations(
        n_players_per_simulation=n_players_per_simulation
    )

    file_name_prefix = str(path_to_unaggregated_directory)
    file_suffix_string = str(file_suffix_number).zfill(3) + file_save_type
    file_for_simulations_results = (
        path_to_simulations
        / base_path_for_n_players
        / path_to_unaggregated_directory
        / f"{file_name_prefix} data {file_suffix_string}"
    )

    return file_for_simulations_results


def make_folder_for_unaggregated_simulations(
    n_players_per_simulation: int,
    path_to_simulations: Path = PATH_TO_SIMULATIONS,
    path_to_unaggregated_directory: Path = PATH_TO_UNAGGREGATED_DATA,
    n_players_path_prefix: str = N_PLAYERS_PATH_PREFIX,
) -> Path:
    base_path_for_n_players = Path(f"{n_players_path_prefix}{n_players_per_simulation}")
    path_to_unaggregated_directory = (
        path_to_simulations / base_path_for_n_players / path_to_unaggregated_directory
    )
    make_dir_if_not_exist(path_to_unaggregated_directory)

    return path_to_unaggregated_directory

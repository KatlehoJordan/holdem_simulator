import math
import os
import shutil
from pathlib import Path

import pandas as pd

from src.card import VALID_CARDS_DICT
from src.config import (
    FILE_SAVE_TYPE,
    N_PLAYERS_PATH_PREFIX,
    N_PLAYERS_TO_SIM_AGG_OR_PLOT,
    PATH_TO_ARCHIVED_SIMULATIONS,
    PATH_TO_SIMULATIONS,
    logger,
)
from src.get_path_for_n_players_aggregated import get_path_for_n_players_aggregated
from src.hole_cards import VALID_HOLE_CARDS_FLAVORS_LIST
from src.make_dir_if_does_not_exist import make_dir_if_not_exist
from src.simulate_hands import (
    N_CARDS_IN_HAND_STRING,
    make_folder_for_unaggregated_simulations,
)

PATH_TO_AGGREGATED_DATA_RESULTS = Path("aggregated")
TOLERANCE_THRESHOLD_FOR_RANDOM_DRAWING = 0.01
MIN_N_APPEARANCES_EXPECTED_OF_EACH_FLAVOR = 1000
TMP_FILE_NAME = f"temp_all_simulations_results{FILE_SAVE_TYPE}"
WINS_BY_PLAYER_STRING = "wins by player"
APPEARANCES_STRING = "appearances"
APPEARANCES_OF_CARDS_STRING = f"{APPEARANCES_STRING} of cards"
HOLE_CARDS_FLAVOR_STRING = "hole cards flavor"
WINS_BY_HOLE_CARDS_FLAVOR_STRING = f"wins by {HOLE_CARDS_FLAVOR_STRING}"
WIN_RATIO_ROUNDED_DOWN_STRING = "win ratio rounded down to nearest 5%"


def aggregate_simulations(
    tmp_file_name: str = TMP_FILE_NAME,
    n_players_to_sim_or_aggregate: int = N_PLAYERS_TO_SIM_AGG_OR_PLOT,
    file_save_type: str = FILE_SAVE_TYPE,
    wins_by_player_string: str = WINS_BY_PLAYER_STRING,
    appearances_of_cards_string: str = APPEARANCES_OF_CARDS_STRING,
    wins_by_hole_cards_flavor_string: str = WINS_BY_HOLE_CARDS_FLAVOR_STRING,
):
    unaggregated_results_folder = make_folder_for_unaggregated_simulations(
        n_players_per_simulation=n_players_to_sim_or_aggregate
    )
    tmp_file_path = unaggregated_results_folder / tmp_file_name

    counter = 0
    for file in unaggregated_results_folder.iterdir():
        if file.suffix == file_save_type:
            df = pd.read_csv(file)
            read_header = counter == 0
            df.to_csv(tmp_file_path, mode="a", index=False, header=read_header)
            counter += 1

    aggregated_wins_by_player_df = _aggregate_wins_by_player(
        tmp_file_path, n_players_simulated_to_aggregate=n_players_to_sim_or_aggregate
    )
    _make_aggregated_file(
        df=aggregated_wins_by_player_df,
        file_name_string_root=wins_by_player_string,
        n_players_simulated_to_aggregate=n_players_to_sim_or_aggregate,
    )

    aggregated_card_appearances_df = _aggregate_appearances_by_card(
        tmp_file_path,
    )
    _make_aggregated_file(
        df=aggregated_card_appearances_df,
        file_name_string_root=appearances_of_cards_string,
        n_players_simulated_to_aggregate=n_players_to_sim_or_aggregate,
    )

    aggregated_wins_by_hole_cards_flavor_df = _aggregate_wins_by_hole_cards_flavor(
        tmp_file_path,
    )
    _make_aggregated_file(
        df=aggregated_wins_by_hole_cards_flavor_df,
        file_name_string_root=wins_by_hole_cards_flavor_string,
        n_players_simulated_to_aggregate=n_players_to_sim_or_aggregate,
    )

    logger.info("Removing the temp file %s", tmp_file_path)
    os.unlink(tmp_file_path)


def _aggregate_wins_by_player(
    file_for_simulations_results: Path,
    n_players_simulated_to_aggregate: int,
    tolerance_threshold_for_random_drawing: float = TOLERANCE_THRESHOLD_FOR_RANDOM_DRAWING,
    wins_by_player_string: str = WINS_BY_PLAYER_STRING,
) -> pd.DataFrame:
    logger.info("Aggregating total %s.", wins_by_player_string)
    data_frame = pd.read_csv(file_for_simulations_results)
    results = [
        _calculate_player_results(
            player,
            data_frame,
            n_players_simulated_to_aggregate,
            tolerance_threshold_for_random_drawing,
        )
        for player in range(n_players_simulated_to_aggregate)
    ]
    player_results_df = pd.DataFrame(results)
    _validate_player_results(player_results_df)
    return player_results_df


def _calculate_player_results(
    player: int,
    data_frame: pd.DataFrame,
    n_players_simulated_to_aggregate: int,
    tolerance_threshold_for_random_drawing: float,
) -> dict:
    wins_as_float_key = (
        f"player_{player}_wins_as_float" if player != 0 else "you_win_as_float"
    )
    this_players_wins = sum(data_frame[wins_as_float_key])
    expected_wins = len(data_frame) / n_players_simulated_to_aggregate
    deviation = this_players_wins - expected_wins
    percent_deviation = abs(deviation) / expected_wins
    deviation_above_tolerable_threshold = (
        percent_deviation > tolerance_threshold_for_random_drawing
    )
    return {
        "player": player,
        "wins": this_players_wins,
        "expected_wins": expected_wins,
        "deviation": deviation,
        "percent_deviation": percent_deviation,
        "deviation_above_tolerable_threshold": deviation_above_tolerable_threshold,
    }


def _validate_player_results(
    out_df: pd.DataFrame,
    tolerance_threshold_for_random_drawing: float = TOLERANCE_THRESHOLD_FOR_RANDOM_DRAWING,
) -> None:
    if not math.isclose(
        out_df["wins"].sum(), out_df["expected_wins"].sum(), rel_tol=1e-9
    ):
        raise ValueError(
            "The total number of wins is not equal to the total number of expected wins. This indicates that perhaps ties are not being handled correctly."
        )
    if not math.isclose(out_df["deviation"].sum(), 0, abs_tol=1e-9):
        raise ValueError(
            "The total deviation is not equal to 0. This indicates that perhaps ties are not being handled correctly."
        )
    if out_df["deviation_above_tolerable_threshold"].any():
        logger.warning(
            f"At least one player's wins deviate from the expected number of wins by more than {tolerance_threshold_for_random_drawing:.0%}. A larger sample should be drawn or else the random assignment of cards to players is not working."
        )


def _aggregate_appearances_by_card(
    file_for_simulations_results: Path,
    n_cards_in_hand_string: str = N_CARDS_IN_HAND_STRING,
    valid_cards_dict: dict = VALID_CARDS_DICT,
    tolerance_threshold_for_random_drawing: float = TOLERANCE_THRESHOLD_FOR_RANDOM_DRAWING,
    appearances_of_cards_string: str = APPEARANCES_OF_CARDS_STRING,
) -> pd.DataFrame:
    logger.info("Aggregating %s.", appearances_of_cards_string)
    data_frame = pd.read_csv(file_for_simulations_results)

    _validate_hand_size(data_frame, n_cards_in_hand_string)

    prob_of_drawing_a_card_in_a_hand = data_frame[n_cards_in_hand_string].iloc[0] / len(
        valid_cards_dict
    )
    results = [
        _calculate_card_results(
            card,
            data_frame,
            prob_of_drawing_a_card_in_a_hand,
            valid_cards_dict,
            tolerance_threshold_for_random_drawing,
        )
        for card in valid_cards_dict
    ]
    aggregated_appearances_by_card_df = pd.DataFrame(results)

    _validate_aggregated_appearances_by_card_results(
        aggregated_appearances_by_card_df, tolerance_threshold_for_random_drawing
    )

    return aggregated_appearances_by_card_df


def _validate_hand_size(data_frame: pd.DataFrame, n_cards_in_hand_string: str):
    if data_frame[n_cards_in_hand_string].nunique() != 1:
        raise ValueError("Not all hands have the same number of cards!")


def _calculate_card_results(
    card: str,
    data_frame: pd.DataFrame,
    prob_of_drawing_a_card_in_a_hand: float,
    valid_cards_dict: dict,
    tolerance_threshold_for_random_drawing: float,
    appearances_string: str = APPEARANCES_STRING,
) -> dict:
    card_name = valid_cards_dict[card].name
    this_card_appearances = sum(data_frame[card_name])
    expected_appearances = len(data_frame) * prob_of_drawing_a_card_in_a_hand
    deviation = this_card_appearances - expected_appearances
    percent_deviation = abs(deviation) / expected_appearances
    deviation_above_tolerable_threshold = (
        percent_deviation > tolerance_threshold_for_random_drawing
    )
    return {
        "card name": card_name,
        appearances_string: this_card_appearances,
        "probability of appearing in a hand": prob_of_drawing_a_card_in_a_hand,
        "expected_appearances": expected_appearances,
        "deviation": deviation,
        "percent_deviation": percent_deviation,
        "deviation_above_tolerable_threshold": deviation_above_tolerable_threshold,
    }


def _validate_aggregated_appearances_by_card_results(
    out_df: pd.DataFrame, tolerance_threshold_for_random_drawing: float
):
    if not math.isclose(
        out_df["appearances"].sum(), out_df["expected_appearances"].sum(), rel_tol=1e-9
    ):
        raise ValueError(
            "The total number of appearances is not equal to the total number of expected appearances. This indicates that perhaps expected appearances are not being calculated correctly."
        )
    if not math.isclose(out_df["deviation"].sum(), 0, abs_tol=1e-9):
        raise ValueError(
            "The total deviation is not equal to 0. This indicates that perhaps expected appearances are not being calculated correctly."
        )
    if out_df["deviation_above_tolerable_threshold"].any():
        logger.warning(
            f"At least one card's appearances deviate from the expected number of appearances by more than {tolerance_threshold_for_random_drawing:.0%}. A larger sample should be drawn or else the random assignment of cards to players is not working."
        )


def _aggregate_wins_by_hole_cards_flavor(
    file_for_simulations_results: Path,
    valid_hole_cards_flavors_list: list = VALID_HOLE_CARDS_FLAVORS_LIST,
    min_n_appearances_expected_of_each_flavor: int = MIN_N_APPEARANCES_EXPECTED_OF_EACH_FLAVOR,
    wins_by_hole_cards_flavor_string: str = WINS_BY_HOLE_CARDS_FLAVOR_STRING,
) -> pd.DataFrame:
    logger.info("Aggregating %s.", wins_by_hole_cards_flavor_string)
    data_frame = pd.read_csv(file_for_simulations_results)
    results = [
        _calculate_hole_card_results(
            hole_cards_flavor, data_frame, min_n_appearances_expected_of_each_flavor
        )
        for hole_cards_flavor in valid_hole_cards_flavors_list
    ]
    aggregated_wins_by_hole_cards_df = pd.DataFrame(results)
    df_sorted_by_win_ratio = aggregated_wins_by_hole_cards_df.sort_values(
        "win ratio", ascending=False
    )
    _validate_appearances_of_hole_cards(
        df_sorted_by_win_ratio, min_n_appearances_expected_of_each_flavor
    )
    return df_sorted_by_win_ratio


def _calculate_hole_card_results(
    hole_cards_flavor: str,
    data_frame: pd.DataFrame,
    min_n_appearances_expected_of_each_flavor: int,
    hole_cards_flavor_string: str = HOLE_CARDS_FLAVOR_STRING,
    appearances_string: str = APPEARANCES_STRING,
    win_ratio_rounded_down_string: str = WIN_RATIO_ROUNDED_DOWN_STRING,
) -> dict:
    this_hole_cards_flavor_appears = sum(data_frame[hole_cards_flavor])
    this_hole_cards_flavor_wins = data_frame.winning_hole_cards_flavors.apply(
        lambda x: x.count(hole_cards_flavor)
    ).sum()
    win_ratio = this_hole_cards_flavor_wins / this_hole_cards_flavor_appears
    win_ratio_rounded_down_to_nearest_5_percent = win_ratio // 0.05 * 0.05
    fewer_than_expected_appearances = (
        this_hole_cards_flavor_appears < min_n_appearances_expected_of_each_flavor
    )
    return {
        hole_cards_flavor_string: hole_cards_flavor,
        appearances_string: this_hole_cards_flavor_appears,
        "wins": this_hole_cards_flavor_wins,
        "win ratio": win_ratio,
        win_ratio_rounded_down_string: win_ratio_rounded_down_to_nearest_5_percent,
        "fewer than expected appearances": fewer_than_expected_appearances,
    }


def _validate_appearances_of_hole_cards(
    df_sorted_by_win_ratio: pd.DataFrame, min_n_appearances_expected_of_each_flavor: int
):
    if df_sorted_by_win_ratio["fewer than expected appearances"].any():
        logger.warning(
            f"At least one hole_card_flavor's appearances are fewer than the expected appearances of  {min_n_appearances_expected_of_each_flavor}. A larger sample should be drawn to get more representation of all hole_card_flavors."
        )


def _make_aggregated_file(
    df: pd.DataFrame,
    file_name_string_root: str,
    n_players_simulated_to_aggregate: int,
    path_to_simulations: Path = PATH_TO_SIMULATIONS,
    n_players_path_prefix: str = N_PLAYERS_PATH_PREFIX,
    path_to_aggregated_directory: Path = PATH_TO_AGGREGATED_DATA_RESULTS,
    path_to_archive: Path = PATH_TO_ARCHIVED_SIMULATIONS,
    file_save_type: str = FILE_SAVE_TYPE,
) -> None:
    file_name_string_root = file_name_string_root
    file_name = f"{file_name_string_root}{file_save_type}"
    path_for_n_players = get_path_for_n_players_aggregated(
        n_players_simulated_to_aggregate=n_players_simulated_to_aggregate,
        path_to_simulations=path_to_simulations,
        n_players_path_prefix=n_players_path_prefix,
    )
    path_for_n_players_archive = path_for_n_players / path_to_archive
    make_dir_if_not_exist(path_for_n_players_archive)
    path_for_n_players_aggregated = path_for_n_players / path_to_aggregated_directory
    make_dir_if_not_exist(path_for_n_players_aggregated)

    file_path_for_results = path_for_n_players_aggregated / file_name
    logger.info("Saving aggregated results to %s", file_path_for_results)
    df.to_csv(file_path_for_results, index=False)

    timestamp = pd.Timestamp.now().strftime("%Y-%m-%d")
    logger.info(
        "Saving timestamped copy of aggregated results to %s with timestamp %s",
        path_for_n_players_archive,
        timestamp,
    )
    subfolder_path = path_for_n_players_archive / Path(file_name).stem
    make_dir_if_not_exist(subfolder_path)
    shutil.copy2(
        file_path_for_results,
        subfolder_path / f"{timestamp}{file_save_type}",
    )

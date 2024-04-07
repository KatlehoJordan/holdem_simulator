import shutil
from pathlib import Path

import pandas as pd

from src.card import VALID_CARDS_DICT
from src.config import (
    PATH_TO_ARCHIVED_SIMULATIONS_DATA_RESULTS,
    PATH_TO_SIMULATIONS_DATA_RESULTS,
    logger,
)
from src.hole_cards import VALID_HOLE_CARDS_FLAVORS_LIST
from src.make_dir_if_does_not_exist import make_dir_if_not_exist
from src.simulate_hands import (
    N_CARDS_IN_HAND_STRING,
    make_file_path_for_unaggregated_simulations,
)

PATH_TO_AGGREGATED_DATA_RESULTS = PATH_TO_SIMULATIONS_DATA_RESULTS / "aggregated"
TOLERANCE_THRESHOLD_FOR_RANDOM_DRAWING = 0.1
N_PLAYERS_SIMULATED_TO_AGGREGATE = 2
MIN_N_APPEARANCES_EXPECTED_OF_EACH_FLAVOR = 1000


def aggregate_simulations(
    n_players_simulated_to_aggregate: int = N_PLAYERS_SIMULATED_TO_AGGREGATE,
    errors_for_low_sample_size: bool = True,
):
    file_path_for_simulations_results = make_file_path_for_unaggregated_simulations(
        n_players_per_simulation=n_players_simulated_to_aggregate
    )
    aggregated_wins_by_player_df = _aggregate_wins_by_player(
        file_path_for_simulations_results,
        error_if_deviation_above_tolerable_threshold=errors_for_low_sample_size,
    )
    _make_aggregated_wins_by_player_file(aggregated_wins_by_player_df)

    aggregated_card_appearances_df = _aggregate_appearances_by_card(
        file_path_for_simulations_results,
        error_if_deviation_above_tolerable_threshold=errors_for_low_sample_size,
    )
    _make_aggregated_card_appearances_file(aggregated_card_appearances_df)

    aggregated_wins_by_hole_cards_flavor_df = _aggregate_wins_by_hole_cards_flavor(
        file_path_for_simulations_results,
        error_if_too_few_of_any_given_flavor=errors_for_low_sample_size,
    )
    _make_aggregated_wins_by_hole_cards_flavor_file(
        aggregated_wins_by_hole_cards_flavor_df
    )


def _aggregate_wins_by_player(
    file_for_simulations_results: Path,
    n_players_simulated_to_aggregate: int = N_PLAYERS_SIMULATED_TO_AGGREGATE,
    tolerance_threshold_for_random_drawing: float = TOLERANCE_THRESHOLD_FOR_RANDOM_DRAWING,
    error_if_deviation_above_tolerable_threshold: bool = True,
) -> pd.DataFrame:
    logger.info("Aggregating total wins by player.")
    data_frame = pd.read_csv(file_for_simulations_results)
    results = []
    for player in range(n_players_simulated_to_aggregate):
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
        results.append(
            {
                "player": player,
                "wins": this_players_wins,
                "expected_wins": expected_wins,
                "deviation": deviation,
                "percent_deviation": percent_deviation,
                "deviation_above_tolerable_threshold": deviation_above_tolerable_threshold,
            }
        )
    out_df = pd.DataFrame(results)
    if error_if_deviation_above_tolerable_threshold:
        if out_df["deviation_above_tolerable_threshold"].any():
            raise ValueError(
                f"At least one player's wins deviate from the expected number of wins by more than {tolerance_threshold_for_random_drawing:.0%}. A larger sample should be drawn or else the random assignment of cards to players is not working."
            )

    return out_df


def _aggregate_appearances_by_card(
    file_for_simulations_results: Path,
    n_cards_in_hand_string: str = N_CARDS_IN_HAND_STRING,
    valid_cards_dict: dict = VALID_CARDS_DICT,
    tolerance_threshold_for_random_drawing: float = TOLERANCE_THRESHOLD_FOR_RANDOM_DRAWING,
    error_if_deviation_above_tolerable_threshold: bool = True,
) -> pd.DataFrame:
    logger.info("Aggregating appearances of each card")
    data_frame = pd.read_csv(file_for_simulations_results)

    if data_frame[n_cards_in_hand_string].nunique() != 1:
        raise ValueError("Not all hands have the same number of cards!")

    prob_of_drawing_a_card_in_a_hand = data_frame[n_cards_in_hand_string].iloc[0] / len(
        valid_cards_dict
    )
    results = []
    for card in valid_cards_dict:
        card_name = valid_cards_dict[card].name
        this_card_appearances = sum(data_frame[card_name])
        expected_appearances = len(data_frame) * prob_of_drawing_a_card_in_a_hand
        deviation = this_card_appearances - expected_appearances
        percent_deviation = abs(deviation) / expected_appearances
        deviation_above_tolerable_threshold = (
            percent_deviation > tolerance_threshold_for_random_drawing
        )
        results.append(
            {
                "card name": card_name,
                "appearances": this_card_appearances,
                "probability of appearing in a hand": prob_of_drawing_a_card_in_a_hand,
                "expected_appearances": expected_appearances,
                "deviation": deviation,
                "percent_deviation": percent_deviation,
                "deviation_above_tolerable_threshold": deviation_above_tolerable_threshold,
            }
        )
    out_df = pd.DataFrame(results)
    if (
        error_if_deviation_above_tolerable_threshold
        and out_df["deviation_above_tolerable_threshold"].any()
    ):
        raise ValueError(
            f"At least one card's appearances deviate from the expected number of appearances by more than {tolerance_threshold_for_random_drawing:.0%}. A larger sample should be drawn or else the random assignment of cards to players is not working."
        )

    return out_df


def _aggregate_wins_by_hole_cards_flavor(
    file_for_simulations_results: Path,
    valid_hole_cards_flavors_list: list = VALID_HOLE_CARDS_FLAVORS_LIST,
    min_n_appearances_expected_of_each_flavor: int = MIN_N_APPEARANCES_EXPECTED_OF_EACH_FLAVOR,
    error_if_too_few_of_any_given_flavor: bool = True,
) -> pd.DataFrame:
    logger.info("Aggregating total wins by hole cards flavor")
    data_frame = pd.read_csv(file_for_simulations_results)
    results = []
    for hole_cards_flavor in valid_hole_cards_flavors_list:
        this_hole_cards_flavor_appears = sum(data_frame[hole_cards_flavor])
        this_hole_cards_flavor_wins = data_frame.winning_hole_cards_flavors.apply(
            lambda x: x.count(hole_cards_flavor)
        ).sum()
        win_ratio = this_hole_cards_flavor_wins / this_hole_cards_flavor_appears
        win_ratio_rounded_down_to_nearest_5_percent = win_ratio // 0.05 * 0.05
        fewer_than_expected_appearances = (
            this_hole_cards_flavor_appears < min_n_appearances_expected_of_each_flavor
        )
        results.append(
            {
                "hole cards flavor": hole_cards_flavor,
                "appearances": this_hole_cards_flavor_appears,
                "wins": this_hole_cards_flavor_wins,
                "win ratio": win_ratio,
                "win ratio rounded down to nearest 5%": win_ratio_rounded_down_to_nearest_5_percent,
                "fewer than expected appearances": fewer_than_expected_appearances,
            }
        )
    out_df = pd.DataFrame(results)
    df_sorted_by_win_ratio = out_df.sort_values("win ratio", ascending=False)
    if (
        error_if_too_few_of_any_given_flavor
        and df_sorted_by_win_ratio["fewer than expected appearances"].any()
    ):
        raise ValueError(
            f"At least one hole_card_flavor's appearances are fewer than the expected appearances of  {min_n_appearances_expected_of_each_flavor}. A larger sample should be drawn to get more representation of all hole_card_flavors."
        )
    return df_sorted_by_win_ratio


def _make_aggregated_file(
    df: pd.DataFrame,
    file_name: str,
    path_to_aggregated_directory: Path = PATH_TO_AGGREGATED_DATA_RESULTS,
    path_to_archive: Path = PATH_TO_ARCHIVED_SIMULATIONS_DATA_RESULTS,
) -> None:
    make_dir_if_not_exist(path_to_archive)
    make_dir_if_not_exist(path_to_aggregated_directory)

    file_path_for_results = path_to_aggregated_directory / file_name

    if file_path_for_results.exists():
        logger.info(
            "%s already exists. Copying it to the archive folder with a timestamp.",
            file_path_for_results,
        )
        timestamp = pd.Timestamp.now().strftime("%Y-%m-%d")
        shutil.copy2(
            file_path_for_results,
            path_to_archive / f"{file_path_for_results.stem} dated {timestamp}.csv",
        )

    else:
        logger.info("%s does not exist. Creating it now.", file_path_for_results)
    df.to_csv(file_path_for_results, index=False)


def _make_aggregated_wins_by_player_file(
    df: pd.DataFrame,
    n_players_simulated_to_aggregate: int = N_PLAYERS_SIMULATED_TO_AGGREGATE,
) -> None:
    file_name = f"aggregated data for {n_players_simulated_to_aggregate} players.csv"
    _make_aggregated_file(df, file_name)


def _make_aggregated_card_appearances_file(
    df: pd.DataFrame,
    n_players_simulated_to_aggregate: int = N_PLAYERS_SIMULATED_TO_AGGREGATE,
) -> None:
    file_name = f"aggregated data for appearances of cards with {n_players_simulated_to_aggregate} players.csv"
    _make_aggregated_file(df, file_name)


def _make_aggregated_wins_by_hole_cards_flavor_file(
    df: pd.DataFrame,
    n_players_simulated_to_aggregate: int = N_PLAYERS_SIMULATED_TO_AGGREGATE,
) -> None:
    file_name = f"aggregated data for wins by hole cards flavor with {n_players_simulated_to_aggregate} players.csv"
    _make_aggregated_file(df, file_name)

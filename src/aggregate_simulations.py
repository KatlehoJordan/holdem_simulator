import shutil
from pathlib import Path

import pandas as pd

from src.config import (
    PATH_TO_ARCHIVED_SIMULATIONS_DATA_RESULTS,
    PATH_TO_SIMULATIONS_DATA_RESULTS,
    logger,
)
from src.make_dir_if_does_not_exist import make_dir_if_not_exist
from src.simulate_hands import make_file_path_for_unaggregated_simulations

PATH_TO_AGGREGATED_DATA_RESULTS = PATH_TO_SIMULATIONS_DATA_RESULTS / "aggregated"
TOLERANCE_THRESHOLD_FOR_RANDOM_DRAWING = 0.1
N_PLAYERS_SIMULATED_TO_AGGREGATE = 2


def aggregate_simulations(
    n_players_simulated_to_aggregate: int = N_PLAYERS_SIMULATED_TO_AGGREGATE,
):
    file_path_for_simulations_results = make_file_path_for_unaggregated_simulations(
        n_players_per_simulation=n_players_simulated_to_aggregate
    )
    aggregated_wins_by_player_df = _aggregate_wins_by_player(
        file_path_for_simulations_results,
        warn_if_deviation_above_tolerable_threshold=False,
    )
    _make_aggregated_results_file(aggregated_wins_by_player_df)
    # TODO: Create similar function as _aggregate_wins_by_player, but for each card appearance, in order to verify they are all appearing with equal frequency.
    # TODO: After the previous, make a summary in order to get %age win for each player, and %age of each unique_card in order to validate your random drawing is working as expected
    # TODO: Measure how frequently each card appears in a hand (should expect a uniform distribution if my random drawing is working correctly)
    # TODO: After previous, calculate %age of each hole_cards_flavor
    logger.debug("pause here")


def _make_aggregated_results_file(
    df: pd.DataFrame,
    path_to_aggregated_directory: Path = PATH_TO_AGGREGATED_DATA_RESULTS,
    path_to_archive: Path = PATH_TO_ARCHIVED_SIMULATIONS_DATA_RESULTS,
    n_players_simulated_to_aggregate: int = N_PLAYERS_SIMULATED_TO_AGGREGATE,
) -> None:
    make_dir_if_not_exist(path_to_archive)
    make_dir_if_not_exist(path_to_aggregated_directory)

    subfolder = path_to_aggregated_directory
    file_name_prefix = "aggregated"
    file_for_simulations_results = (
        subfolder
        / f"{file_name_prefix} data for {n_players_simulated_to_aggregate} players.csv"
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

    else:
        logger.info("%s does not exist. Creating it now.", file_for_simulations_results)
    df.to_csv(file_for_simulations_results, index=False)


def _aggregate_wins_by_player(
    file_for_simulations_results: Path,
    n_players_simulated_to_aggregate: int = N_PLAYERS_SIMULATED_TO_AGGREGATE,
    tolerance_threshold_for_random_drawing: float = TOLERANCE_THRESHOLD_FOR_RANDOM_DRAWING,
    warn_if_deviation_above_tolerable_threshold: bool = True,
) -> pd.DataFrame:
    logger.info("Aggregating total wins")
    data_frame = pd.read_csv(file_for_simulations_results)
    total_wins = 0.0
    out_df = pd.DataFrame()
    for player in range(n_players_simulated_to_aggregate):
        wins_as_float_key = (
            f"player_{player}_wins_as_float" if player != 0 else "you_win_as_float"
        )
        this_players_wins = sum(data_frame[wins_as_float_key])
        expected_wins = len(data_frame) / n_players_simulated_to_aggregate
        deviation = this_players_wins - expected_wins
        percent_deviation = abs(deviation) / expected_wins
        if percent_deviation > tolerance_threshold_for_random_drawing:
            deviation_above_tolerable_threshold = True
        else:
            deviation_above_tolerable_threshold = False
        total_wins += this_players_wins
        out_df = pd.concat(
            [
                out_df,
                pd.DataFrame(
                    [
                        {
                            "player": player,
                            "wins": this_players_wins,
                            "expected_wins": expected_wins,
                            "deviation": deviation,
                            "percent_deviation": percent_deviation,
                            "deviation_above_tolerable_threshold": deviation_above_tolerable_threshold,
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )
    if warn_if_deviation_above_tolerable_threshold:
        if out_df["deviation_above_tolerable_threshold"].any():
            raise ValueError(
                f"At least one player's wins deviate from the expected number of wins by more than {tolerance_threshold_for_random_drawing:.0%}. A larger sample should be drawn or else the random assignment of cards to players is not working."
            )

    return out_df

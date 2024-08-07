from datetime import datetime
from math import e
from pathlib import Path

import pandas as pd

from src.config import DATA_PATH, SHOULD_CALL_STRING, logger
from src.guess_result import GuessResult
from src.hand import Hand

TRAINING_RESULTS_PATH = Path(f"{DATA_PATH}/training_results")

SUMMARY_STRING = "All"

N_PLAYERS_OPTIONS = [
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    SUMMARY_STRING,
]

N_PLAYERS_STRING = "N Players"
N_HANDS_STRING = "N Hands"
N_CORRECT_STRING = "N Correct"
N_TO_CALL_STRING = "N to Call"
N_TO_CALL_CORRECT_STRING = "N to Call Correct"
N_TO_FOLD_STRING = "N to Fold"
N_TO_FOLD_CORRECT_STRING = "N to Fold Correct"

COLUMNS_TO_INIT_WITH_INT_0 = [
    N_HANDS_STRING,
    N_CORRECT_STRING,
    N_TO_CALL_STRING,
    N_TO_CALL_CORRECT_STRING,
    N_TO_FOLD_STRING,
    N_TO_FOLD_CORRECT_STRING,
]

PERCENT_HANDS_CORRECT_STRING = "% Hands Correct"
PERCENT_TO_CALL_CORRECT_STRING = "% to Call Correct"
PERCENT_TO_FOLD_CORRECT_STRING = "% to Fold Correct"

PERCENT_COLUMNS = [
    PERCENT_HANDS_CORRECT_STRING,
    PERCENT_TO_CALL_CORRECT_STRING,
    PERCENT_TO_FOLD_CORRECT_STRING,
]

PLAY_STYLE_STRING = "Play style"

THRESHOLD_FOR_GREAT_PLAY = 0.95

WORSE_PLAY_STYLE = "Inaccurate in All Ways"
TIGHT_PLAY_STYLE = "Too Tight"
LOOSE_PLAY_STYLE = "Too Loose"
GREAT_PLAY_STYLE = "Great Play"

COLUMNS_FOR_TRAINING_RESULTS = (
    [N_PLAYERS_STRING]
    + COLUMNS_TO_INIT_WITH_INT_0
    + PERCENT_COLUMNS
    + [PLAY_STYLE_STRING]
)


def save_train_results(
    hand: Hand,
    hand_guess_result: GuessResult,
    should_call_string: str = SHOULD_CALL_STRING,
) -> None:
    _make_train_results_if_needed()
    dataframe = _read_training_results_csv()
    dataframe = _increment_n_hands(
        dataframe=dataframe, n_players_int=hand.n_players_in_the_hand
    )

    if hand.should_call == should_call_string:
        dataframe = _increment_n_to_call(
            dataframe=dataframe, n_players_int=hand.n_players_in_the_hand
        )
    else:
        dataframe = _increment_n_to_fold(
            dataframe=dataframe, n_players_int=hand.n_players_in_the_hand
        )

    if hand_guess_result == GuessResult.CORRECT:
        dataframe = _increment_n_correct(
            dataframe=dataframe, n_players_int=hand.n_players_in_the_hand
        )
        if hand.should_call == should_call_string:
            dataframe = _increment_n_to_call_correct(
                dataframe=dataframe, n_players_int=hand.n_players_in_the_hand
            )
        else:
            dataframe = _increment_n_to_fold_correct(
                dataframe=dataframe, n_players_int=hand.n_players_in_the_hand
            )

    dataframe = _calculate_percent_cols(dataframe)
    dataframe = _format_percent_cols(dataframe)
    _save_df_to_csv(dataframe=dataframe)


def _save_df_to_csv(dataframe):
    todays_csv_string = _make_todays_csv_string()
    dataframe.to_csv(todays_csv_string, index=False)


def _read_training_results_csv() -> pd.DataFrame:
    logger.info("Reading training results csv into dataframe.")
    todays_csv_string = _make_todays_csv_string()
    return pd.read_csv(todays_csv_string)


def _make_train_results_if_needed() -> None:
    logger.info("Making today's training results if it does not exist.")
    if not _check_if_todays_csv_exists():
        _make_train_results_csv()
    else:
        logger.info("Today's training results already exist; did not create.")


def _make_train_results_csv() -> None:
    logger.info("Making training results csv.")
    df = _initialize_training_results_df()
    todays_csv_string = _make_todays_csv_string()
    df.to_csv(todays_csv_string, index=False)


def _initialize_training_results_df(
    columns: list[str] = COLUMNS_FOR_TRAINING_RESULTS,
    n_players_column: str = N_PLAYERS_STRING,
    n_players_options: list[str] = N_PLAYERS_OPTIONS,
) -> pd.DataFrame:
    logger.info("Initializing training results dataframe.")
    df = pd.DataFrame(columns=columns)
    n_players_df = pd.DataFrame(n_players_options, columns=[n_players_column])
    df = pd.concat([df, n_players_df], ignore_index=True)
    df[COLUMNS_TO_INIT_WITH_INT_0] = 0
    return df


def _make_todays_csv_string(
    training_results_path: Path = TRAINING_RESULTS_PATH,
) -> str:
    logger.info("Making today's csv string.")
    todays_date = datetime.today().strftime("%Y-%m-%d")
    todays_csv_string = f"{training_results_path}/{todays_date}.csv"
    return todays_csv_string


def _check_if_todays_csv_exists() -> bool:
    logger.info("Checking if today's csv exists.")
    todays_csv_string = _make_todays_csv_string()
    return Path(todays_csv_string).exists()


def _increment_n_hands(
    dataframe: pd.DataFrame,
    n_players_int: int,
    n_hands_string: str = N_HANDS_STRING,
) -> pd.DataFrame:
    return _increment_column(
        dataframe,
        n_hands_string,
        str(n_players_int),
    )


def _increment_n_correct(
    dataframe: pd.DataFrame,
    n_players_int: int,
    n_correct_string: str = N_CORRECT_STRING,
) -> pd.DataFrame:
    return _increment_column(
        dataframe,
        n_correct_string,
        str(n_players_int),
    )


def _increment_n_to_call(
    dataframe: pd.DataFrame,
    n_players_int: int,
    n_to_call_string: str = N_TO_CALL_STRING,
) -> pd.DataFrame:
    return _increment_column(
        dataframe,
        n_to_call_string,
        str(n_players_int),
    )


def _increment_n_to_fold(
    dataframe: pd.DataFrame,
    n_players_int: int,
    n_to_fold_string: str = N_TO_FOLD_STRING,
) -> pd.DataFrame:
    return _increment_column(
        dataframe,
        n_to_fold_string,
        str(n_players_int),
    )


def _increment_n_to_call_correct(
    dataframe: pd.DataFrame,
    n_players_int: int,
    n_to_call_correct_string: str = N_TO_CALL_CORRECT_STRING,
) -> pd.DataFrame:
    return _increment_column(
        dataframe,
        n_to_call_correct_string,
        str(n_players_int),
    )


def _increment_n_to_fold_correct(
    dataframe: pd.DataFrame,
    n_players_int: int,
    n_to_fold_correct_string: str = N_TO_FOLD_CORRECT_STRING,
) -> pd.DataFrame:
    return _increment_column(
        dataframe,
        n_to_fold_correct_string,
        str(n_players_int),
    )


def _increment_column(
    dataframe: pd.DataFrame,
    column_string: str,
    n_players: str,
    summary_string: str = SUMMARY_STRING,
) -> pd.DataFrame:
    logger.info(f"Updating df column: {column_string}")
    dataframe = _increment_cell(
        dataframe,
        column_string,
        n_players,
    )
    dataframe = _increment_cell(
        dataframe,
        column_string,
        n_players=summary_string,
    )
    return dataframe


def _increment_cell(
    dataframe: pd.DataFrame,
    column_string: str,
    n_players: str,
    n_players_string: str = N_PLAYERS_STRING,
) -> pd.DataFrame:
    logger.info(f"Updating for {n_players} players.")
    mask = dataframe[n_players_string] == n_players
    dataframe.loc[mask, column_string] = dataframe.loc[mask, column_string]
    dataframe.loc[mask, column_string] += 1
    return dataframe


def _calculate_percent_cols(dataframe: pd.DataFrame):
    dataframe = _calculate_percent_hands_correct(dataframe)
    dataframe = _calculate_percent_to_call_correct(dataframe)
    dataframe = _calculate_percent_to_fold_correct(dataframe)
    dataframe = _calculate_play_style(dataframe)
    return dataframe


def _calculate_percent_hands_correct(
    dataframe: pd.DataFrame,
    n_correct_string: str = N_CORRECT_STRING,
    n_hands_string: str = N_HANDS_STRING,
    new_column_string: str = PERCENT_HANDS_CORRECT_STRING,
) -> pd.DataFrame:
    return _calculate_percentage_column(
        dataframe,
        numerator_column_string=n_correct_string,
        denominator_column_string=n_hands_string,
        new_column_string=new_column_string,
    )


def _calculate_percent_to_call_correct(
    dataframe: pd.DataFrame,
    n_to_call_correct_string: str = N_TO_CALL_CORRECT_STRING,
    n_to_call_string: str = N_TO_CALL_STRING,
    new_column_string: str = PERCENT_TO_CALL_CORRECT_STRING,
) -> pd.DataFrame:
    return _calculate_percentage_column(
        dataframe,
        numerator_column_string=n_to_call_correct_string,
        denominator_column_string=n_to_call_string,
        new_column_string=new_column_string,
    )


def _calculate_percent_to_fold_correct(
    dataframe: pd.DataFrame,
    n_to_fold_correct_string: str = N_TO_FOLD_CORRECT_STRING,
    n_to_fold_string: str = N_TO_FOLD_STRING,
    new_column_string: str = PERCENT_TO_FOLD_CORRECT_STRING,
) -> pd.DataFrame:
    return _calculate_percentage_column(
        dataframe,
        numerator_column_string=n_to_fold_correct_string,
        denominator_column_string=n_to_fold_string,
        new_column_string=new_column_string,
    )


def _calculate_percentage_column(
    dataframe: pd.DataFrame,
    numerator_column_string: str,
    denominator_column_string: str,
    new_column_string: str,
):
    logger.info(f"Calculating {new_column_string} column.")
    dataframe[new_column_string] = (
        dataframe[numerator_column_string] / dataframe[denominator_column_string]
    )
    return dataframe


def _calculate_play_style(
    dataframe: pd.DataFrame,
    percent_hands_correct_string: str = PERCENT_HANDS_CORRECT_STRING,
    percent_to_call_correct_string: str = PERCENT_TO_CALL_CORRECT_STRING,
    percent_to_fold_correct_string: str = PERCENT_TO_FOLD_CORRECT_STRING,
    play_style_string: str = PLAY_STYLE_STRING,
    threshold_for_great_play: float = THRESHOLD_FOR_GREAT_PLAY,
    worse_play_style_string: str = WORSE_PLAY_STYLE,
    tight_play_style_string: str = TIGHT_PLAY_STYLE,
    loose_play_style_string: str = LOOSE_PLAY_STYLE,
    great_play_style_string: str = GREAT_PLAY_STYLE,
) -> pd.DataFrame:
    logger.info("Calculating play style.")

    dataframe[play_style_string] = worse_play_style_string

    mask = (
        (dataframe[percent_hands_correct_string] > threshold_for_great_play)
        & (dataframe[percent_to_call_correct_string] > threshold_for_great_play)
        & (dataframe[percent_to_fold_correct_string] <= threshold_for_great_play)
    )
    dataframe.loc[mask, play_style_string] = loose_play_style_string

    mask = (
        (dataframe[percent_hands_correct_string] > threshold_for_great_play)
        & (dataframe[percent_to_call_correct_string] <= threshold_for_great_play)
        & (dataframe[percent_to_fold_correct_string] > threshold_for_great_play)
    )
    dataframe.loc[mask, play_style_string] = tight_play_style_string

    mask = (
        (dataframe[percent_hands_correct_string] > threshold_for_great_play)
        & (dataframe[percent_to_call_correct_string] > threshold_for_great_play)
        & (dataframe[percent_to_fold_correct_string] > threshold_for_great_play)
    )
    dataframe.loc[mask, play_style_string] = great_play_style_string

    return dataframe


def _format_percent_cols(
    dataframe: pd.DataFrame, percent_columns: list[str] = PERCENT_COLUMNS
) -> pd.DataFrame:
    dataframe[percent_columns] = dataframe[percent_columns].apply(
        lambda col: col.map(lambda x: f"{x:.2%}")
    )
    return dataframe

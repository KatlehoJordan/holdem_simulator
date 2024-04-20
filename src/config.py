import logging
from pathlib import Path

DATA_PATH = Path("data")

MIN_SMALL_BLIND = 10
VALID_SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]

RAW_RANK_VALUE_STRING = "raw_rank_value"
N_POSSIBLE_STRAIGHTS_STRING = "n_possible_straights"
N_PLAYERS_TO_SIM_OR_AGGREGATE = 9
N_SIMS = int(
    100_000 / N_PLAYERS_TO_SIM_OR_AGGREGATE
)  # >420 000 total is likely needed to get over 1000 appearances for each hole_cards_flavor

NUMBER_OF_CARDS_IN_QUALIFYING_HAND = 6
ACE_AS_LOW_RAW_RANK_VALUE = 1
ACE_AS_HIGH_RAW_RANK_VALUE = 14
N_PLAYERS_PATH_PREFIX = "n_players_"
PATH_TO_SIMULATIONS = Path("simulations")
PATH_TO_ARCHIVED_SIMULATIONS = Path("archived_simulations")
FILE_SAVE_TYPE = ".csv"

VALID_RANKS_DICT = {
    "2": {
        RAW_RANK_VALUE_STRING: 2,
        N_POSSIBLE_STRAIGHTS_STRING: 2,
    },
    "3": {
        RAW_RANK_VALUE_STRING: 3,
        N_POSSIBLE_STRAIGHTS_STRING: 3,
    },
    "4": {
        RAW_RANK_VALUE_STRING: 4,
        N_POSSIBLE_STRAIGHTS_STRING: 4,
    },
    "5": {
        RAW_RANK_VALUE_STRING: 5,
        N_POSSIBLE_STRAIGHTS_STRING: 5,
    },
    "6": {
        RAW_RANK_VALUE_STRING: 6,
        N_POSSIBLE_STRAIGHTS_STRING: 5,
    },
    "7": {
        RAW_RANK_VALUE_STRING: 7,
        N_POSSIBLE_STRAIGHTS_STRING: 5,
    },
    "8": {
        RAW_RANK_VALUE_STRING: 8,
        N_POSSIBLE_STRAIGHTS_STRING: 5,
    },
    "9": {
        RAW_RANK_VALUE_STRING: 9,
        N_POSSIBLE_STRAIGHTS_STRING: 5,
    },
    "10": {
        RAW_RANK_VALUE_STRING: 10,
        N_POSSIBLE_STRAIGHTS_STRING: 5,
    },
    "Jack": {
        RAW_RANK_VALUE_STRING: 11,
        N_POSSIBLE_STRAIGHTS_STRING: 4,
    },
    "Queen": {
        RAW_RANK_VALUE_STRING: 12,
        N_POSSIBLE_STRAIGHTS_STRING: 3,
    },
    "King": {
        RAW_RANK_VALUE_STRING: 13,
        N_POSSIBLE_STRAIGHTS_STRING: 2,
    },
    "Ace": {
        RAW_RANK_VALUE_STRING: ACE_AS_HIGH_RAW_RANK_VALUE,
        N_POSSIBLE_STRAIGHTS_STRING: 2,
    },
}


def find_key_by_raw_rank_value(
    input_integer: int,
    valid_ranks_dict: dict[str, dict[str, int]] = VALID_RANKS_DICT,
    raw_rank_value_string: str = RAW_RANK_VALUE_STRING,
) -> str:
    if input_integer < 2 or input_integer > 14:
        return "Invalid rank value"
    else:
        for key, value in valid_ranks_dict.items():
            if value[raw_rank_value_string] == input_integer:
                return key
    return "Rank not found"


# logging.addLevelName(5, "CUSTOM")
# logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
# logger = logging.getLogger()

# def custom(self, message, *args, **kws):
#     if self.isEnabledFor(5):
#         self._log(5, message, args, **kws)

# logging.Logger.custom = custom

########

import logging


class CustomLogger(logging.Logger):
    def simulating(self, message, *args, **kws):
        if self.isEnabledFor(25):
            self._log(25, message, args, **kws)


logging.setLoggerClass(CustomLogger)
logging.addLevelName(25, "SIMULATING")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger: CustomLogger = logging.getLogger(__name__)  # type: ignore because Pylance does not recognize that the custom logger class can inherit from the base logger class

logger.simulating("This is a custom log message")

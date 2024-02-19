import random

from src.config import MAX_PLAYERS_AHEAD_OF_YOU, MIN_PLAYERS_AHEAD_OF_YOU, logger


class PlayersAheadOfYou:
    def __init__(self, n_players_ahead_of_you: int):
        if (
            n_players_ahead_of_you < MIN_PLAYERS_AHEAD_OF_YOU
            or n_players_ahead_of_you > MAX_PLAYERS_AHEAD_OF_YOU
            or n_players_ahead_of_you % 1 != 0
        ):
            raise ValueError(
                f"n_players_ahead_of_you must be between {MIN_PLAYERS_AHEAD_OF_YOU} and {MAX_PLAYERS_AHEAD_OF_YOU} and an integer."
            )
        self.n = n_players_ahead_of_you
        logger.info(f"{self}")

    def __str__(self):
        return f"Players ahead of you: {self.n}"


def select_random_n_players_ahead_of_you():
    n_players = random.randint(
        MIN_PLAYERS_AHEAD_OF_YOU,
        MAX_PLAYERS_AHEAD_OF_YOU,
    )
    return PlayersAheadOfYou(n_players)

import numpy as np

from src.config import logger

MIN_PLAYERS_AHEAD_OF_YOU = 1
MAX_PLAYERS_AHEAD_OF_YOU = 9


class PlayersAheadOfYou:
    def __init__(
        self,
        n_players_ahead_of_you: int,
        min_players_ahead_of_you: int = MIN_PLAYERS_AHEAD_OF_YOU,
        max_players_ahead_of_you: int = MAX_PLAYERS_AHEAD_OF_YOU,
    ):
        if (
            n_players_ahead_of_you < min_players_ahead_of_you
            or n_players_ahead_of_you > max_players_ahead_of_you
            or n_players_ahead_of_you % 1 != 0
        ):
            raise ValueError(
                f"n_players_ahead_of_you must be between {min_players_ahead_of_you} and {max_players_ahead_of_you} and an integer."
            )
        self.n = n_players_ahead_of_you
        logger.info("%s\n", self)

    def __str__(self):
        return f"Players ahead of you: {self.n}"

    @classmethod
    def select_n_players(
        cls,
        min_players_ahead_of_you: int = MIN_PLAYERS_AHEAD_OF_YOU,
        max_players_ahead_of_you: int = MAX_PLAYERS_AHEAD_OF_YOU,
    ) -> "PlayersAheadOfYou":
        players = range(min_players_ahead_of_you, max_players_ahead_of_you + 1)
        probabilities = [1 / (i**0.75) for i in players]
        probabilities = [p / sum(probabilities) for p in probabilities]
        n_players = np.random.choice(players, p=probabilities)
        return cls(n_players)

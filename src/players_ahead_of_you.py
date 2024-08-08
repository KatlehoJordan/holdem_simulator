import numpy as np

from src.config import N_PLAYERS_STRING, logger

# MIN_PLAYERS_AHEAD_OF_YOU = 1
# TODO: If not training (e.g., if simulating more hands for aggregating data), then set MIN_PLAYERS_AHEAD_OF_YOU to 1
MIN_PLAYERS_AHEAD_OF_YOU = 2
MAX_PLAYERS_AHEAD_OF_YOU = 9


class PlayersAheadOfYou:
    def __init__(
        self,
        n_players_ahead_of_you: int,
        min_players_ahead_of_you: int = MIN_PLAYERS_AHEAD_OF_YOU,
        max_players_ahead_of_you: int = MAX_PLAYERS_AHEAD_OF_YOU,
        n_players_string: str = N_PLAYERS_STRING,
    ):
        if (
            n_players_ahead_of_you < min_players_ahead_of_you
            or n_players_ahead_of_you > max_players_ahead_of_you
            or n_players_ahead_of_you % 1 != 0
        ):
            raise ValueError(
                f"{n_players_string}_ahead_of_you must be between {min_players_ahead_of_you} and {max_players_ahead_of_you} and an integer."
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
        probabilities = probabilities[::-1]
        n_players = np.random.choice(players, p=probabilities)
        return cls(n_players)

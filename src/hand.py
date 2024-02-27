import math
import random
from typing import Tuple, Union

from src.active_player import ActivePlayer
from src.bet import Bet
from src.big_blind import BigBlind
from src.config import logger
from src.players_ahead_of_you import PlayersAheadOfYou
from src.small_blind import SmallBlind

N_PLAYERS_IN_BLINDS = 2


class Hand:
    def __init__(
        self,
        n_players: Union[PlayersAheadOfYou, None] = None,
        small_blind: Union[SmallBlind, None] = None,
    ):
        if n_players is None:
            n_players = PlayersAheadOfYou.select_n_players()
        if small_blind is None:
            small_blind = SmallBlind.select_random_small_blind()
        if not isinstance(n_players, PlayersAheadOfYou):
            raise ValueError(
                f"n_players must be a PlayersAheadOfYou, not {type(n_players)}"
            )
        if not isinstance(small_blind, SmallBlind):
            raise ValueError(
                f"small_blind must be a SmallBlind, not {type(small_blind)}"
            )
        self.max_bet = BigBlind(small_blind).amount
        self.pot_size = small_blind.amount + self.max_bet
        self.pot_odds = calculate_pot_odds(self.max_bet, self.pot_size)
        self.pot_size, self.pot_odds = simulate_bets_for_players_ahead_of_you(
            n_players, self.max_bet, self.pot_size, self.pot_odds
        )

    def show_pot_size(self):
        logger.info("Pot size:")
        logger.info("%s", self.pot_size)

    def show_pot_odds(self):
        logger.info("Max bet:")
        logger.info("%s", self.max_bet)
        logger.info("Pot size:")
        logger.info("%s", self.pot_size)
        logger.info("Pot odds:")
        logger.info(
            "%s >= %s / (%s + %s)",
            self.pot_odds,
            self.max_bet,
            self.max_bet,
            self.pot_size,
        )


def round_up_to_nearest_5_percent(x: float) -> str:
    if x * 20 % 1 == 0:
        rounded = x
    else:
        rounded = math.ceil(x * 20) / 20
    return "{:.0f}%".format(rounded * 100)


def calculate_pot_odds(max_bet: int, pot_size: int) -> str:
    return round_up_to_nearest_5_percent(max_bet / (pot_size + max_bet))


def simulate_bets_for_players_ahead_of_you(
    n_players: PlayersAheadOfYou,
    max_bet: int,
    pot_size: int,
    pot_odds: str,
    n_players_in_blinds: int = N_PLAYERS_IN_BLINDS,
) -> Tuple[int, str]:
    prob_double_max_bet = 1 / n_players.n
    prob_triple_max_bet = prob_double_max_bet / n_players.n
    prob_call = 1 - prob_double_max_bet - prob_triple_max_bet
    choices = ["double", "triple", "call"]
    probabilities = [prob_double_max_bet, prob_triple_max_bet, prob_call]
    for _ in range(n_players_in_blinds, n_players.n):
        n_player = _ + 1
        choice = random.choices(choices, probabilities, k=1)[0]
        if choice == "double":
            max_bet *= 2
        elif choice == "triple":
            max_bet *= 3
        ActivePlayer(bet=Bet(max_bet))
        logger.info(f"Player {n_player} bets {max_bet}")
        pot_size += max_bet
        pot_odds = calculate_pot_odds(max_bet, pot_size)
    return pot_size, pot_odds

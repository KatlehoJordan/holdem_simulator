import math
import random

from src.active_player import ActivePlayer
from src.bet import Bet
from src.big_blind import BigBlind
from src.config import N_PLAYERS_IN_BLINDS, logger
from src.players_ahead_of_you import PlayersAheadOfYou
from src.small_blind import SmallBlind


def round_up_to_nearest_5_percent(x: float) -> str:
    if x * 20 % 1 == 0:
        rounded = x
    else:
        rounded = math.ceil(x * 20) / 20
    return "{:.0f}%".format(rounded * 100)


class Hand:
    def __init__(
        self,
        n_players: PlayersAheadOfYou = PlayersAheadOfYou.select_n_players(),
        small_blind: SmallBlind = SmallBlind.make_random_small_blind(),
    ):
        self.max_bet = BigBlind(small_blind).amount
        self.pot_size = small_blind.amount + self.max_bet
        self.pot_odds = self.calculate_pot_odds()
        self.simulate_bets_for_players_ahead_of_you(n_players)

    def calculate_pot_odds(self):
        return round_up_to_nearest_5_percent(
            self.max_bet / (self.pot_size + self.max_bet)
        )

    def simulate_bets_for_players_ahead_of_you(self, n_players: PlayersAheadOfYou):
        prob_double_max_bet = 1 / n_players.n
        prob_triple_max_bet = prob_double_max_bet / n_players.n
        prob_call = 1 - prob_double_max_bet - prob_triple_max_bet
        choices = ["double", "triple", "call"]
        probabilities = [prob_double_max_bet, prob_triple_max_bet, prob_call]
        for _ in range(N_PLAYERS_IN_BLINDS, n_players.n):
            n_player = _ + 1
            choice = random.choices(choices, probabilities, k=1)[0]
            if choice == "double":
                self.max_bet *= 2
            elif choice == "triple":
                self.max_bet *= 3
            ActivePlayer(bet=Bet(self.max_bet))
            logger.info(f"Player {n_player} bets {self.max_bet}")
            self.pot_size += self.max_bet
            self.pot_odds = self.calculate_pot_odds()

    def show_pot_size(self):
        logger.info(f"Pot size: {self.pot_size}")

    def show_pot_odds(self):
        logger.info(
            f"You need at least this probability to win to justify playing: {self.pot_odds}"
        )

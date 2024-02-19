import random

from src.active_player import ActivePlayer
from src.bet import Bet
from src.big_blind import BigBlind
from src.config import N_PLAYERS_IN_BLINDS, logger
from src.players_ahead_of_you import PlayersAheadOfYou
from src.small_blind import SmallBlind


class Hand:
    def __init__(
        self,
        n_players: PlayersAheadOfYou = PlayersAheadOfYou.select_n_players(),
        small_blind: SmallBlind = SmallBlind.make_random_small_blind(),
    ):
        self.big_blind = BigBlind(small_blind)
        self.pot_size = small_blind.amount + self.big_blind.amount
        self.simulate_bets_for_players_ahead_of_you(n_players)

    def simulate_bets_for_players_ahead_of_you(self, n_players: PlayersAheadOfYou):
        current_max_bet = self.big_blind.amount
        prob_double_max_bet = 1 / n_players.n
        prob_triple_max_bet = prob_double_max_bet / n_players.n
        prob_call = 1 - prob_double_max_bet - prob_triple_max_bet
        choices = ["double", "triple", "call"]
        probabilities = [prob_double_max_bet, prob_triple_max_bet, prob_call]
        for _ in range(N_PLAYERS_IN_BLINDS, n_players.n):
            choice = random.choices(choices, probabilities, k=1)[0]
            if choice == "double":
                current_max_bet *= 2
            elif choice == "triple":
                current_max_bet *= 3
            ActivePlayer(bet=Bet(current_max_bet))
            logger.info(f"Player {_ + 1} bets {current_max_bet}")
            self.pot_size += current_max_bet

    def show_pot_size(self):
        logger.info(f"Pot size: {self.pot_size}")

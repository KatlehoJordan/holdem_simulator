import math
import random
from typing import Dict, List, Tuple, Union

from community_cards import CommunityCards
from src.active_player import ActivePlayer
from src.bet import Bet
from src.big_blind import BigBlind
from src.config import logger
from src.deck import Deck
from src.hole_cards import HoleCards
from src.player_hand import PlayerHand
from src.players_ahead_of_you import PlayersAheadOfYou
from src.small_blind import SmallBlind

N_PLAYERS_IN_BLINDS = 2


class Hand:
    def __init__(
        self,
        n_players_ahead_of_you: Union[PlayersAheadOfYou, None] = None,
        small_blind: Union[SmallBlind, None] = None,
    ):
        if n_players_ahead_of_you is None:
            n_players_ahead_of_you = PlayersAheadOfYou.select_n_players()
        if small_blind is None:
            small_blind = SmallBlind.select_random_small_blind()
        if not isinstance(n_players_ahead_of_you, PlayersAheadOfYou):
            raise ValueError(
                f"n_players must be a PlayersAheadOfYou type, not {type(n_players_ahead_of_you)}"
            )
        if not isinstance(small_blind, SmallBlind):
            raise ValueError(
                f"small_blind must be a SmallBlind type, not {type(small_blind)}"
            )
        self.max_bet = BigBlind(small_blind).amount
        self.pot_size = small_blind.amount + self.max_bet
        self.pot_odds = calculate_pot_odds(self.max_bet, self.pot_size)
        self.pot_size, self.pot_odds = simulate_bets_for_players_ahead_of_you(
            n_players_ahead_of_you, self.max_bet, self.pot_size, self.pot_odds
        )
        deck = Deck()
        self.community_cards = CommunityCards(deck=deck)
        self.your_hole_cards = HoleCards(deck=deck)
        self.hole_cards_for_players_ahead_of_you = (
            simulate_hole_cards_for_players_ahead_of_you(
                n_players_ahead_of_you=n_players_ahead_of_you, deck=deck
            )
        )

        cards_in_the_hand = (
            [self.your_hole_cards.hi_card]
            + [self.your_hole_cards.lo_card]
            + [
                hole_card.hi_card
                for hole_card in self.hole_cards_for_players_ahead_of_you.values()
            ]
            + [
                hole_card.lo_card
                for hole_card in self.hole_cards_for_players_ahead_of_you.values()
            ]
            + self.community_cards.cards
        )
        if len(cards_in_the_hand) != len(set(cards_in_the_hand)):
            raise ValueError("There are non-unique cards in the hand.")

        self.your_player_hand = PlayerHand(
            hole_cards=self.your_hole_cards, community_cards=self.community_cards
        )
        self.player_hands_for_players_ahead_of_you = (
            simulate_player_hands_for_players_head_of_you(
                community_cards=self.community_cards,
                dict_of_hole_cards=self.hole_cards_for_players_ahead_of_you,
            )
        )

        player_hands_in_the_hand = [
            [self.your_player_hand]
            + [
                player_hand
                for player_hand in self.player_hands_for_players_ahead_of_you.values()
            ]
        ]
        if len(player_hands_in_the_hand) != len(set(player_hands_in_the_hand)):
            raise ValueError("There are non-unique hands in the hand.")
        if len(player_hands_in_the_hand) < 2:
            raise ValueError("There must be at least 2 player's hands in the hand.")

        # TODO: Add logic to this class cycle over the compare_player_hands function to determine the winner and or ties, saving an attribute for the best_hand and the 'hole_cards_flavor'.
        # TODO: Extract result in terms of winning or tying hands, losing hands, and number of players for later tabulating during simulation of 1000s of hands

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


def simulate_hole_cards_for_players_ahead_of_you(
    n_players_ahead_of_you: PlayersAheadOfYou,
    deck: Deck,
) -> Dict[str, HoleCards]:
    hole_cards = {}
    for player in range(n_players_ahead_of_you.n):
        player_n = f"Player {player + 1}"
        player_n_hole_cards = HoleCards(
            deck=deck, card1=deck.draw_card(), card2=deck.draw_card()
        )
        logger.info("%s has hole cards: %s", player_n, player_n_hole_cards.name)
        hole_cards[player_n] = player_n_hole_cards
    return hole_cards


def simulate_player_hands_for_players_head_of_you(
    community_cards: CommunityCards,
    dict_of_hole_cards: Dict[str, HoleCards],
) -> Dict[str, PlayerHand]:
    player_hands = {}
    for player, hole_cards in dict_of_hole_cards.items():
        player_n = player
        player_n_hand = PlayerHand(
            hole_cards=hole_cards, community_cards=community_cards
        )
        logger.info("%s has a %s", player_n, player_n_hand.hand_type.name)
        player_hands[player_n] = player_n_hand
    return player_hands

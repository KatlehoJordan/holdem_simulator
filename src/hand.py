import math
import random
from typing import Dict, List, Tuple, Union

from src.active_player import ActivePlayer
from src.bet import Bet
from src.big_blind import BigBlind
from src.community_cards import CommunityCards
from src.config import logger
from src.deck import Deck
from src.hole_cards import HoleCards
from src.player_hand import (
    FIRST_PLAYER_WINS_STRING,
    PLAYERS_TIE_STRING,
    SECOND_PLAYER_WINS_STRING,
    PlayerHand,
    compare_player_hands,
)
from src.players_ahead_of_you import PlayersAheadOfYou
from src.small_blind import SmallBlind

N_PLAYERS_IN_BLINDS = 2
HAND_WINNER_FLAVOR = "Single winner"
HAND_TIE_FLAVOR = "Tie"


class Hand:
    def __init__(
        self,
        n_players_ahead_of_you: Union[PlayersAheadOfYou, None] = None,
        small_blind: Union[SmallBlind, None] = None,
    ):
        (
            self.pot_odds,
            self.max_bet,
            self.pot_size,
            self.player_hands_in_the_hand,
            self.winning_hands,
            self.losing_hands,
            self.winning_type,
            self.name,
        ) = _assign_hand_attributes(
            n_players_ahead_of_you=n_players_ahead_of_you,
            small_blind=small_blind,
        )
        logger.info("%s\n", self)

    def __str__(self):
        return f"\n{self.name}"

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


def _init_n_players_and_small_blind(
    n_players_ahead_of_you: Union[PlayersAheadOfYou, None],
    small_blind: Union[SmallBlind, None],
) -> Tuple[PlayersAheadOfYou, SmallBlind]:
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

    return n_players_ahead_of_you, small_blind


def _ensure_cards_in_hand_are_unique(
    your_hole_cards: HoleCards,
    hole_cards_for_players_ahead_of_you: Dict[str, HoleCards],
    community_cards: CommunityCards,
) -> None:
    cards_in_the_hand = (
        [your_hole_cards.hi_card]
        + [your_hole_cards.lo_card]
        + [
            hole_card.hi_card
            for hole_card in hole_cards_for_players_ahead_of_you.values()
        ]
        + [
            hole_card.lo_card
            for hole_card in hole_cards_for_players_ahead_of_you.values()
        ]
        + community_cards.cards
    )
    if len(cards_in_the_hand) != len(set(cards_in_the_hand)):
        raise ValueError("There are non-unique cards in the hand.")


def _round_up_to_nearest_5_percent(x: float) -> str:
    if x * 20 % 1 == 0:
        rounded = x
    else:
        rounded = math.ceil(x * 20) / 20
    return "{:.0f}%".format(rounded * 100)


def _calculate_pot_odds(max_bet: int, pot_size: int) -> str:
    return _round_up_to_nearest_5_percent(max_bet / (pot_size + max_bet))


def _simulate_bets_for_players_ahead_of_you(
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
        pot_odds = _calculate_pot_odds(max_bet, pot_size)
    return pot_size, pot_odds


def _simulate_hole_cards_for_players_ahead_of_you(
    n_players_ahead_of_you: PlayersAheadOfYou,
    deck: Deck,
) -> Dict[str, HoleCards]:
    hole_cards = {}
    for player in range(n_players_ahead_of_you.n):
        player_n = f"Player {player + 1}"
        player_n_hole_cards = HoleCards(
            deck=deck,
            whose_cards=f"{player_n}'s",
            card1=deck.draw_card(),
            card2=deck.draw_card(),
        )
        logger.debug("%s has hole cards: %s", player_n, player_n_hole_cards.name)
        hole_cards[player_n] = player_n_hole_cards
    return hole_cards


def _simulate_player_hands_for_players_head_of_you(
    community_cards: CommunityCards,
    dict_of_hole_cards: Dict[str, HoleCards],
) -> Dict[str, PlayerHand]:
    player_hands = {}
    for player, hole_cards in dict_of_hole_cards.items():
        player_n_hand = PlayerHand(
            hole_cards=hole_cards,
            community_cards=community_cards,
            whose_cards=f"{player}'s",
        )
        logger.debug("%s has a %s", player, player_n_hand.hand_type.name)
        player_hands[player] = player_n_hand
    return player_hands


def _make_name_strings(
    n_players_in_the_hand: int,
    community_cards: CommunityCards,
    winning_type: str,
    winning_hands: list[PlayerHand],
    losing_hands: list[PlayerHand],
) -> str:
    n_players_string = f"\nN players in hand:\n{n_players_in_the_hand}\n"
    community_cards_string = f"\nCommunity cards:\n{community_cards.name}\n"
    winning_type_string = f"\nWinning type:\n{winning_type}.\n"
    winning_hands_string = f"\nWinning hand(s):\n{winning_hands[0]}\n"
    losing_hands_string = (
        "\nLosing hand(s):\n" + "\n".join(str(hand) for hand in losing_hands) + "\n"
    )
    winning_hole_cards_string = (
        f"\nWinning hole cards: {winning_hands[0].hole_cards}.\n"
    )
    losing_hole_cards_string = "\nLosing hole cards:" + "\n".join(
        str(hand.hole_cards) for hand in losing_hands
    )
    name_string = f"{n_players_string}{community_cards_string}{winning_type_string}{winning_hands_string}{losing_hands_string}{winning_hole_cards_string}{losing_hole_cards_string}"

    return name_string


def _ensure_player_hands_are_valid(player_hands_in_the_hand: list[PlayerHand]) -> None:
    if len(player_hands_in_the_hand) != len(set(player_hands_in_the_hand)):
        raise ValueError("There are non-unique hands in the hand.")
    if len(player_hands_in_the_hand) < 2:
        raise ValueError("There must be at least 2 player's hands in the hand.")


def _determine_winners_and_losers(
    player_hands_in_the_hand: List[PlayerHand],
    first_player_wins_string: str = FIRST_PLAYER_WINS_STRING,
    second_player_wins_string: str = SECOND_PLAYER_WINS_STRING,
    players_tie_string: str = PLAYERS_TIE_STRING,
    hand_winner_flavor: str = HAND_WINNER_FLAVOR,
    hand_tie_flavor: str = HAND_TIE_FLAVOR,
) -> Tuple[List[PlayerHand], List[PlayerHand], str]:
    current_best_hand = player_hands_in_the_hand[0]
    winning_hands = []
    winning_type = ""
    for player_hand in player_hands_in_the_hand[1:]:
        comparison_result = compare_player_hands(current_best_hand, player_hand)
        if comparison_result == first_player_wins_string:
            winning_hands = [current_best_hand]
            winning_type = hand_winner_flavor
        elif comparison_result == second_player_wins_string:
            current_best_hand = player_hand
            winning_hands = [current_best_hand]
            winning_type = hand_winner_flavor
        elif comparison_result == players_tie_string:
            winning_hands.append(player_hand)
            winning_type = hand_tie_flavor
    losing_hands = [
        player_hand
        for player_hand in player_hands_in_the_hand
        if player_hand not in winning_hands
    ]

    return winning_hands, losing_hands, winning_type


def _init_cards_and_bets(
    n_players_ahead_of_you: Union[PlayersAheadOfYou, None] = None,
    small_blind: Union[SmallBlind, None] = None,
) -> Tuple[int, int, HoleCards, int, str, CommunityCards, Dict[str, HoleCards]]:
    n_players_ahead_of_you, small_blind = _init_n_players_and_small_blind(
        n_players_ahead_of_you, small_blind
    )
    max_bet = BigBlind(small_blind).amount
    deck = Deck()
    your_hole_cards = HoleCards(deck=deck)
    pot_size = small_blind.amount + max_bet
    pot_odds = _calculate_pot_odds(max_bet, pot_size)
    pot_size, pot_odds = _simulate_bets_for_players_ahead_of_you(
        n_players_ahead_of_you, max_bet, pot_size, pot_odds
    )
    community_cards = CommunityCards(deck=deck)
    hole_cards_for_players_ahead_of_you = _simulate_hole_cards_for_players_ahead_of_you(
        n_players_ahead_of_you=n_players_ahead_of_you, deck=deck
    )

    n_players_in_the_hand = n_players_ahead_of_you.n + 1

    _ensure_cards_in_hand_are_unique(
        your_hole_cards=your_hole_cards,
        hole_cards_for_players_ahead_of_you=hole_cards_for_players_ahead_of_you,
        community_cards=community_cards,
    )

    return (
        n_players_in_the_hand,
        max_bet,
        your_hole_cards,
        pot_size,
        pot_odds,
        community_cards,
        hole_cards_for_players_ahead_of_you,
    )


def _determine_player_hands(
    your_hole_cards: HoleCards,
    community_cards: CommunityCards,
    hole_cards_for_players_ahead_of_you: Dict[str, HoleCards],
) -> List[PlayerHand]:
    your_player_hand = PlayerHand(
        hole_cards=your_hole_cards, community_cards=community_cards
    )
    player_hands_for_players_ahead_of_you = (
        _simulate_player_hands_for_players_head_of_you(
            community_cards=community_cards,
            dict_of_hole_cards=hole_cards_for_players_ahead_of_you,
        )
    )

    player_hands_in_the_hand = [your_player_hand] + [
        player_hand for player_hand in player_hands_for_players_ahead_of_you.values()
    ]

    _ensure_player_hands_are_valid(player_hands_in_the_hand)

    return player_hands_in_the_hand


def _assign_hand_attributes(
    n_players_ahead_of_you: Union[PlayersAheadOfYou, None] = None,
    small_blind: Union[SmallBlind, None] = None,
) -> Tuple[
    str, int, int, List[PlayerHand], List[PlayerHand], List[PlayerHand], str, str
]:
    (
        n_players_in_the_hand,
        max_bet,
        your_hole_cards,
        pot_size,
        pot_odds,
        community_cards,
        hole_cards_for_players_ahead_of_you,
    ) = _init_cards_and_bets(
        n_players_ahead_of_you=n_players_ahead_of_you, small_blind=small_blind
    )

    player_hands_in_the_hand = _determine_player_hands(
        your_hole_cards=your_hole_cards,
        community_cards=community_cards,
        hole_cards_for_players_ahead_of_you=hole_cards_for_players_ahead_of_you,
    )

    winning_hands, losing_hands, winning_type = _determine_winners_and_losers(
        player_hands_in_the_hand,
    )

    # TODO: Add logic to this function to cycle over the compare_player_hands function to determine the winner and or ties, saving an attribute for the best_hand and the 'hole_cards_flavor'.
    # TODO: Extract result in terms of winning or tying hands, losing hands, and number of players for later tabulating during simulation of 1000s of hands
    name = _make_name_strings(
        n_players_in_the_hand,
        community_cards,
        winning_type,
        winning_hands,
        losing_hands,
    )

    return (
        pot_odds,
        max_bet,
        pot_size,
        player_hands_in_the_hand,
        winning_hands,
        losing_hands,
        winning_type,
        name,
    )

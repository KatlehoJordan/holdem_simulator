import math
import random
from typing import Dict, Tuple, Union

from src.active_player import ActivePlayer
from src.bet import Bet
from src.big_blind import BigBlind
from src.card import Card
from src.community_cards import CommunityCards
from src.config import (
    HAND_WINNER_FLAVOR,
    HOLE_CARDS_FLAVOR_STRING,
    N_PLAYERS_STRING,
    logger,
)
from src.deck import Deck
from src.hole_cards import HoleCards
from src.player_hand import (
    PLAYERS_TIE_STRING,
    SECOND_PLAYER_WINS_STRING,
    PlayerHand,
    compare_player_hands,
)
from src.players_ahead_of_you import PlayersAheadOfYou
from src.small_blind import SmallBlind

N_PLAYERS_IN_BLINDS = 2
HAND_TIE_FLAVOR = "Tie"
BASELINE_PROBABILITY_OF_HOLE_CARDS = "<5%"
SHOULD_CALL_STRING = 't'
SHOULD_NOT_CALL_STRING = 'f'


class Hand:
    def __init__(
        self,
        n_players_ahead_of_you: Union[PlayersAheadOfYou, None] = None,
        small_blind: Union[SmallBlind, None] = None,
    ):
        (
            self.prob_needed_to_call,
            self.max_bet,
            self.pot_size,
            self.all_cards_in_the_hand,
            self.player_hands_in_the_hand,
            self.winning_type,
            self.winning_hands,
            self.losing_hands,
            self.winning_hole_cards_flavors,
            self.losing_hole_cards_flavors,
            self.name,
            self.n_players_in_the_hand,
            self.bets,
            self.deck,
            self.your_hole_cards,
            self.hole_cards_prob_to_win,
            self.should_call,
        ) = _assign_hand_attributes(
            n_players_ahead_of_you=n_players_ahead_of_you,
            small_blind=small_blind,
        )
        logger.info("%s\n", self)

    def __str__(self):
        return f"\n{self.name}"

    def show_max_bet(self):
        logger.train("Max bet: %s\n", self.max_bet)

    def show_pot_size(self):
        logger.train("Pot size: %s\n", self.pot_size)

    def show_info_for_finding_prob_needed_to_call(self):
        self.show_max_bet()
        self.show_pot_size()

    def show_prob_needed_to_call(self):
        logger.train(
            "Win probability needed to call:\n\n\t%s >= %s / (%s + %s)",
            self.prob_needed_to_call,
            self.max_bet,
            self.max_bet,
            self.pot_size,
        )

    def show_n_players_in_the_hand(self):
        logger.train("N players in the hand: %s\n", self.n_players_in_the_hand)

    def show_bets(self):
        logger.train("All bets are: %s\n", self.bets)

    def show_your_hole_cards(self):
        self.show_n_players_in_the_hand()
        logger.train("%s\n", self.your_hole_cards.name)

    def show_prob_to_win(self):
        logger.train("Probability to win: %s\n", self.hole_cards_prob_to_win)

    def show_info_for_finding_if_should_call(self):
        self.show_bets()
        self.show_your_hole_cards()

    def show_if_should_call(self, should_call_string: str = SHOULD_CALL_STRING):
        if self.should_call == should_call_string:
            logger.train("You should call the bet")
        else:
            logger.train("You should not call the bet")

def _init_n_players_and_small_blind(
    n_players_ahead_of_you: Union[PlayersAheadOfYou, None],
    small_blind: Union[SmallBlind, None],
) -> Tuple[PlayersAheadOfYou, SmallBlind]:
    if n_players_ahead_of_you is None:
        n_players_ahead_of_you = PlayersAheadOfYou.select_n_players()
    if small_blind is None:
        small_blind = SmallBlind.select_random_small_blind()

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
    scaled_value = x * 20
    rounded_scaled_value = math.ceil(scaled_value)
    value_rounded_up_to_nearest_5 = rounded_scaled_value / 20
    return "{:.0f}%".format(value_rounded_up_to_nearest_5 * 100)


def _calc_prob_needed_to_call(max_bet: int, pot_size: int) -> str:
    return _round_up_to_nearest_5_percent(max_bet / (max_bet + pot_size))


def _simulate_bets_for_players_ahead_of_you(
    n_players: PlayersAheadOfYou,
    big_blind: int,
    pot_size: int,
    n_players_in_blinds: int = N_PLAYERS_IN_BLINDS,
    baseline_prob_of_hole_cards: str = BASELINE_PROBABILITY_OF_HOLE_CARDS,
) -> Tuple[int, str, list[int]]:
    prob_double_max_bet = 1 / n_players.n
    prob_triple_max_bet = prob_double_max_bet / n_players.n
    prob_call = 1 - prob_double_max_bet - prob_triple_max_bet
    choices = ["double", "triple", "call"]
    probabilities = [prob_double_max_bet, prob_triple_max_bet, prob_call]
    big_blind = big_blind
    small_blind = int(big_blind / 2)
    bets = [small_blind, big_blind]
    prob_needed_to_call = baseline_prob_of_hole_cards
    if n_players.n <= 2:
        prob_needed_to_call = _calc_prob_needed_to_call(big_blind, pot_size)
    else:
        for _ in range(n_players_in_blinds, n_players.n):
            n_player = _ + 1
            choice = random.choices(choices, probabilities, k=1)[0]
            if choice == "double":
                big_blind *= 2
            elif choice == "triple":
                big_blind *= 3
            bets.append(big_blind)
            ActivePlayer(bet=Bet(big_blind))
            logger.info("Player %s bets %s\n", n_player, big_blind)
            pot_size += big_blind
            prob_needed_to_call = _calc_prob_needed_to_call(big_blind, pot_size)

    if prob_needed_to_call == baseline_prob_of_hole_cards:
        raise ValueError(
            f"Probability needed to call cannot be {baseline_prob_of_hole_cards}. Bets were {bets} and pot size was {pot_size}. Calculated prob_needed_to_call was {_calc_prob_needed_to_call(big_blind, pot_size)}. n_players_in_blinds was {n_players_in_blinds}. n_players was {n_players.n}."
        )

    return pot_size, prob_needed_to_call, bets


def _simulate_hole_cards_for_players_ahead_of_you(
    n_players_ahead_of_you: PlayersAheadOfYou,
    deck: Deck,
) -> Dict[str, HoleCards]:
    hole_cards = {}
    for player in range(n_players_ahead_of_you.n):
        player_n = f"Player {player + 1}"
        player_n_hole_cards = HoleCards(
            deck=deck,
            hole_card_1=deck.draw_card(),
            hole_card_2=deck.draw_card(),
            whose_cards=f"{player_n}'s",
        )
        logger.debug("%s has hole cards: %s", player_n, player_n_hole_cards.name)
        hole_cards[player_n] = player_n_hole_cards
    return hole_cards


def _assign_player_hands_for_players_head_of_you(
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
    losing_hands_string = "\nLosing hand(s):\n" + "\n".join(
        str(hand) for hand in losing_hands
    )
    winning_hole_cards_string = "\n\nWinning hole cards:" + "\n".join(
        str(hand.hole_cards) for hand in winning_hands
    )
    losing_hole_cards_string = "\n\nLosing hole cards:" + "\n".join(
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
    player_hands_in_the_hand: list[PlayerHand],
    second_player_wins_string: str = SECOND_PLAYER_WINS_STRING,
    players_tie_string: str = PLAYERS_TIE_STRING,
    hand_winner_flavor: str = HAND_WINNER_FLAVOR,
    hand_tie_flavor: str = HAND_TIE_FLAVOR,
) -> Tuple[str, list[PlayerHand], list[PlayerHand], list[str], list[str]]:
    winning_type = ""
    current_best_hand = player_hands_in_the_hand[0]
    winning_hands = [current_best_hand]
    winning_hole_cards_flavors = [current_best_hand.hole_cards.hole_cards_flavor]

    for player_hand in player_hands_in_the_hand[1:]:
        head_to_head_result = compare_player_hands(current_best_hand, player_hand)

        if head_to_head_result == players_tie_string:
            winning_hands.append(player_hand)
            winning_hole_cards_flavors.append(player_hand.hole_cards.hole_cards_flavor)

        elif head_to_head_result == second_player_wins_string:
            current_best_hand = player_hand
            winning_hands = [current_best_hand]
            winning_hole_cards_flavors = [
                current_best_hand.hole_cards.hole_cards_flavor
            ]

    overall_comparison_result = compare_player_hands(*player_hands_in_the_hand)
    if overall_comparison_result == players_tie_string:
        winning_type = hand_tie_flavor
        if len(winning_hands) <= 1:
            raise ValueError(
                "There must be more than one winning hand in the case of a tie."
            )
    else:
        winning_type = hand_winner_flavor

    losing_hands = [
        player_hand
        for player_hand in player_hands_in_the_hand
        if player_hand not in winning_hands
    ]
    losing_hole_cards_flavors = [
        player_hand.hole_cards.hole_cards_flavor for player_hand in losing_hands
    ]

    return (
        winning_type,
        winning_hands,
        losing_hands,
        winning_hole_cards_flavors,
        losing_hole_cards_flavors,
    )


def _init_cards_and_bets(
    n_players_ahead_of_you: Union[PlayersAheadOfYou, None] = None,
    small_blind: Union[SmallBlind, None] = None,
) -> Tuple[
    int, int, HoleCards, int, str, CommunityCards, Dict[str, HoleCards], list[int], Deck
]:
    n_players_ahead_of_you, small_blind = _init_n_players_and_small_blind(
        n_players_ahead_of_you, small_blind
    )
    big_blind = BigBlind(small_blind).amount
    deck = Deck()
    your_hole_cards = HoleCards(deck=deck)
    pot_size = small_blind.amount + big_blind
    prob_needed_to_call = _calc_prob_needed_to_call(big_blind, pot_size)
    pot_size, prob_needed_to_call, bets = _simulate_bets_for_players_ahead_of_you(
        n_players_ahead_of_you,
        big_blind,
        pot_size,
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

    max_bet = bets[-1]

    return (
        n_players_in_the_hand,
        max_bet,
        your_hole_cards,
        pot_size,
        prob_needed_to_call,
        community_cards,
        hole_cards_for_players_ahead_of_you,
        bets,
        deck,
    )


def _make_list_of_all_cards_and_determine_player_hands(
    your_hole_cards: HoleCards,
    community_cards: CommunityCards,
    hole_cards_for_players_ahead_of_you: Dict[str, HoleCards],
) -> Tuple[list[Card], list[PlayerHand]]:
    all_cards_in_the_hand = (
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

    your_player_hand = PlayerHand(
        hole_cards=your_hole_cards, community_cards=community_cards
    )
    player_hands_for_players_ahead_of_you = (
        _assign_player_hands_for_players_head_of_you(
            community_cards=community_cards,
            dict_of_hole_cards=hole_cards_for_players_ahead_of_you,
        )
    )

    player_hands_in_the_hand = [your_player_hand] + [
        player_hand for player_hand in player_hands_for_players_ahead_of_you.values()
    ]

    _ensure_player_hands_are_valid(player_hands_in_the_hand)

    return all_cards_in_the_hand, player_hands_in_the_hand


def _assign_hand_attributes(
    n_players_ahead_of_you: Union[PlayersAheadOfYou, None] = None,
    small_blind: Union[SmallBlind, None] = None,
    hole_cards_flavor_string: str = HOLE_CARDS_FLAVOR_STRING,
    n_players_string: str = N_PLAYERS_STRING,
    should_call_string: str = SHOULD_CALL_STRING,
    should_not_call_string: str = SHOULD_NOT_CALL_STRING,
) -> Tuple[
    str,
    int,
    int,
    list[Card],
    list[PlayerHand],
    str,
    list[PlayerHand],
    list[PlayerHand],
    list[str],
    list[str],
    str,
    int,
    list[int],
    Deck,
    HoleCards,
    str,
    str,
]:
    (
        n_players_in_the_hand,
        max_bet,
        your_hole_cards,
        pot_size,
        prob_needed_to_call,
        community_cards,
        hole_cards_for_players_ahead_of_you,
        bets,
        deck,
    ) = _init_cards_and_bets(
        n_players_ahead_of_you=n_players_ahead_of_you, small_blind=small_blind,
    )

    all_cards_in_the_hand, player_hands_in_the_hand = (
        _make_list_of_all_cards_and_determine_player_hands(
            your_hole_cards=your_hole_cards,
            community_cards=community_cards,
            hole_cards_for_players_ahead_of_you=hole_cards_for_players_ahead_of_you,
        )
    )

    (
        winning_type,
        winning_hands,
        losing_hands,
        winning_hole_cards_flavors,
        losing_hole_cards_flavors,
    ) = _determine_winners_and_losers(
        player_hands_in_the_hand,
    )

    name = _make_name_strings(
        n_players_in_the_hand,
        community_cards,
        winning_type,
        winning_hands,
        losing_hands,
    )

    hole_cards_prob_to_win = _extract_hole_cards_prob_to_win(hole_cards_flavor_string, n_players_string, n_players_in_the_hand, your_hole_cards)

    hole_cards_prob_to_win_float = float(hole_cards_prob_to_win.strip('%')) / 100
    prob_needed_to_call_float = float(prob_needed_to_call.strip('%')) / 100

    should_call = should_call_string if hole_cards_prob_to_win_float >= prob_needed_to_call_float else should_not_call_string

    return (
        prob_needed_to_call,
        max_bet,
        pot_size,
        all_cards_in_the_hand,
        player_hands_in_the_hand,
        winning_type,
        winning_hands,
        losing_hands,
        winning_hole_cards_flavors,
        losing_hole_cards_flavors,
        name,
        n_players_in_the_hand,
        bets,
        deck,
        your_hole_cards,
        hole_cards_prob_to_win,
        should_call,
    )

def _extract_hole_cards_prob_to_win(hole_cards_flavor_string, n_players_string, n_players_in_the_hand, your_hole_cards):
    # TODO: Move this import to top, and then untie the circular dependency it creates
    from src.get_rounded_win_prob_for_hole_cards_and_players import (
        get_rounded_win_prob_for_hole_cards_and_players,
    )

    df = get_rounded_win_prob_for_hole_cards_and_players()
    filtered_df = df[(df[n_players_string] == n_players_in_the_hand) &
        (df[hole_cards_flavor_string] == your_hole_cards.hole_cards_flavor)
        ]

    hole_cards_prob_to_win = f"{filtered_df.iloc[0]["win ratio rounded down to nearest 5%"] * 100:.0f}%"
    return hole_cards_prob_to_win

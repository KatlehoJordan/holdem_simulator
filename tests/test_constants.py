from src.deck import Deck
from src.hole_cards import HoleCards
from src.scaling_constants import (
    OTHER_SUBTRACTION_CONSTANT_AFTER_SHRINKING,
    SUBTRACTION_CONSTANT_AFTER_SHRINKING,
    VALUE_OF_POCKET_ACES_BEFORE_SHRINKING,
    VALUE_OF_WEAKEST_HAND_STILL_IN_TOP_50PCT_OF_HANDS_BEFORE_SHRINKING,
)
from tests.tests_config import VALID_CARDS_DICT

# TODO: Build tests that confirm the following are in the right order (%age at 2 players, %age at 10 players):
# Aces paired (85, 30) > Kings paired (80, 20) > Jacks paired (75, 15) > 8s paired (70, 10) > King, 3 off suit (50, 5)
# 10s paired (75, 15) > 7s paired (65, 10) > King, 3 off suit (50, 5)
# 9s paired (70, 15) > Ace, 4 suited (60, 10) > King, 3 off suit (50, 5)
# Ace, King suited (65, 20) > Queen, 10 suited (55, 15) > King, 3 off suit (50, 5)
# King, Queen suited (65, 15) > Ace, 4 suited (60, 10) > Queen, 7 off suit (50, 5)
# Ace, Jack suited (65, 15) > Queen, Jack off suit (55, 10) > King, 3 off suit (50, 5)
# King, Jack suited (60, 15) > Queen, Jack off suit (55, 10) > 8, 3 suited (40, 5)
# Queen, 10 suited (55, 15) > 3s paired (50, 10) >  Jack, 5 off suit (45, 5)


# TODO: Implement these tests by removing the prefix underscores or consider deprecating this entire file
PAIR_OF_FIVES = HoleCards(
    deck=Deck(),
    hole_card_1=VALID_CARDS_DICT["5_OF_SPADES"],
    hole_card_2=VALID_CARDS_DICT["5_OF_DIAMONDS"],
)
KING_QUEEN_SUITED = HoleCards(
    deck=Deck(),
    hole_card_1=VALID_CARDS_DICT["KING_OF_SPADES"],
    hole_card_2=VALID_CARDS_DICT["QUEEN_OF_SPADES"],
)
PAIR_OF_FOURS = HoleCards(
    deck=Deck(),
    hole_card_1=VALID_CARDS_DICT["4_OF_SPADES"],
    hole_card_2=VALID_CARDS_DICT["4_OF_DIAMONDS"],
)
FIVE_FOUR_SUITED = HoleCards(
    deck=Deck(),
    hole_card_1=VALID_CARDS_DICT["5_OF_SPADES"],
    hole_card_2=VALID_CARDS_DICT["4_OF_SPADES"],
)
PAIR_OF_TWOS = HoleCards(
    deck=Deck(),
    hole_card_1=VALID_CARDS_DICT["2_OF_SPADES"],
    hole_card_2=VALID_CARDS_DICT["2_OF_DIAMONDS"],
)
KING_QUEEN_OFF_SUIT = HoleCards(
    deck=Deck(),
    hole_card_1=VALID_CARDS_DICT["KING_OF_SPADES"],
    hole_card_2=VALID_CARDS_DICT["QUEEN_OF_DIAMONDS"],
)
FOUR_THREE_SUITED = HoleCards(
    deck=Deck(),
    hole_card_1=VALID_CARDS_DICT["4_OF_SPADES"],
    hole_card_2=VALID_CARDS_DICT["3_OF_SPADES"],
)
PAIR_OF_ACES = HoleCards(
    deck=Deck(),
    hole_card_1=VALID_CARDS_DICT["ACE_OF_SPADES"],
    hole_card_2=VALID_CARDS_DICT["ACE_OF_DIAMONDS"],
)
ACE_QUEEN_OFF_SUIT = HoleCards(
    deck=Deck(),
    hole_card_1=VALID_CARDS_DICT["ACE_OF_SPADES"],
    hole_card_2=VALID_CARDS_DICT["QUEEN_OF_DIAMONDS"],
)
ACE_JACK_SUITED = HoleCards(
    deck=Deck(),
    hole_card_1=VALID_CARDS_DICT["ACE_OF_SPADES"],
    hole_card_2=VALID_CARDS_DICT["JACK_OF_SPADES"],
)
ACE_NINE_SUITED = HoleCards(
    deck=Deck(),
    hole_card_1=VALID_CARDS_DICT["ACE_OF_SPADES"],
    hole_card_2=VALID_CARDS_DICT["9_OF_SPADES"],
)
EIGHT_SEVEN_SUITED = HoleCards(
    deck=Deck(),
    hole_card_1=VALID_CARDS_DICT["8_OF_SPADES"],
    hole_card_2=VALID_CARDS_DICT["7_OF_SPADES"],
)
SEVEN_TWO_OFF_SUIT = HoleCards(
    deck=Deck(),
    hole_card_1=VALID_CARDS_DICT["7_OF_SPADES"],
    hole_card_2=VALID_CARDS_DICT["2_OF_DIAMONDS"],
)
SIX_FIVE_OFF_SUIT = HoleCards(
    deck=Deck(),
    hole_card_1=VALID_CARDS_DICT["6_OF_SPADES"],
    hole_card_2=VALID_CARDS_DICT["5_OF_DIAMONDS"],
)
FOUR_TWO_OFF_SUIT = HoleCards(
    deck=Deck(),
    hole_card_1=VALID_CARDS_DICT["4_OF_SPADES"],
    hole_card_2=VALID_CARDS_DICT["2_OF_DIAMONDS"],
)
THREE_TWO_OFF_SUIT = HoleCards(
    deck=Deck(),
    hole_card_1=VALID_CARDS_DICT["3_OF_SPADES"],
    hole_card_2=VALID_CARDS_DICT["2_OF_DIAMONDS"],
)


def _test_pair_bonus():
    assert PAIR_OF_FIVES.summed_value > KING_QUEEN_SUITED.summed_value
    assert KING_QUEEN_SUITED.summed_value > PAIR_OF_FOURS.summed_value
    assert FIVE_FOUR_SUITED.summed_value > PAIR_OF_TWOS.summed_value
    assert PAIR_OF_TWOS.summed_value > KING_QUEEN_OFF_SUIT.summed_value
    assert PAIR_OF_TWOS.summed_value > FOUR_THREE_SUITED.summed_value


def _test_flush_potential_bonus_not_too_high():
    assert ACE_QUEEN_OFF_SUIT.summed_value > ACE_JACK_SUITED.summed_value


def _test_centrality_bonus_not_too_high():
    assert ACE_JACK_SUITED.summed_value > ACE_NINE_SUITED.summed_value


def _test_straight_potential_bonus_not_too_high():
    assert SEVEN_TWO_OFF_SUIT.summed_value > SIX_FIVE_OFF_SUIT.summed_value


def _test_obvious_dominance():
    assert FOUR_TWO_OFF_SUIT.summed_value > THREE_TWO_OFF_SUIT.summed_value


def _test_pair_aces_match_constant():
    assert PAIR_OF_ACES.summed_value == VALUE_OF_POCKET_ACES_BEFORE_SHRINKING


def _test_weakest_hand_in_top_50pct_matches_constant():
    assert (
        EIGHT_SEVEN_SUITED.summed_value
        == VALUE_OF_WEAKEST_HAND_STILL_IN_TOP_50PCT_OF_HANDS_BEFORE_SHRINKING
    )


def _test_subtraction_factors_match():
    assert (
        SUBTRACTION_CONSTANT_AFTER_SHRINKING
        == OTHER_SUBTRACTION_CONSTANT_AFTER_SHRINKING
    )

from src.hole_cards import HoleCards
from src.scaling_constants import (
    OTHER_SUBTRACTION_CONSTANT_AFTER_SHRINKING,
    SUBTRACTION_CONSTANT_AFTER_SHRINKING,
    VALUE_OF_POCKET_ACES_BEFORE_SHRINKING,
    VALUE_OF_WEAKEST_HAND_STILL_IN_TOP_50PCT_OF_HANDS_BEFORE_SHRINKING,
)
from tests.tests_config import (
    ACE_OF_DIAMONDS,
    ACE_OF_SPADES,
    EIGHT_OF_SPADES,
    FIVE_OF_DIAMONDS,
    FIVE_OF_SPADES,
    FOUR_OF_DIAMONDS,
    FOUR_OF_SPADES,
    JACK_OF_SPADES,
    KING_OF_SPADES,
    NINE_OF_SPADES,
    QUEEN_OF_DIAMONDS,
    QUEEN_OF_SPADES,
    SEVEN_OF_SPADES,
    SIX_OF_SPADES,
    THREE_OF_SPADES,
    TWO_OF_DIAMONDS,
    TWO_OF_SPADES,
)

PAIR_OF_FIVES = HoleCards(card1=FIVE_OF_SPADES, card2=FIVE_OF_DIAMONDS)
KING_QUEEN_SUITED = HoleCards(card1=KING_OF_SPADES, card2=QUEEN_OF_SPADES)
PAIR_OF_FOURS = HoleCards(card1=FOUR_OF_SPADES, card2=FOUR_OF_DIAMONDS)
FIVE_FOUR_SUITED = HoleCards(card1=FIVE_OF_SPADES, card2=FOUR_OF_SPADES)
PAIR_OF_TWOS = HoleCards(card1=TWO_OF_SPADES, card2=TWO_OF_DIAMONDS)
KING_QUEEN_OFF_SUIT = HoleCards(card1=KING_OF_SPADES, card2=QUEEN_OF_DIAMONDS)
FOUR_THREE_SUITED = HoleCards(card1=FOUR_OF_SPADES, card2=THREE_OF_SPADES)
PAIR_OF_ACES = HoleCards(card1=ACE_OF_SPADES, card2=ACE_OF_DIAMONDS)
ACE_QUEEN_OFF_SUIT = HoleCards(card1=ACE_OF_SPADES, card2=QUEEN_OF_DIAMONDS)
ACE_JACK_SUITED = HoleCards(card1=ACE_OF_SPADES, card2=JACK_OF_SPADES)
ACE_NINE_SUITED = HoleCards(card1=ACE_OF_SPADES, card2=NINE_OF_SPADES)
EIGHT_SEVEN_SUITED = HoleCards(card1=EIGHT_OF_SPADES, card2=SEVEN_OF_SPADES)
SEVEN_TWO_OFF_SUIT = HoleCards(card1=SEVEN_OF_SPADES, card2=TWO_OF_DIAMONDS)
SIX_FIVE_OFF_SUIT = HoleCards(card1=SIX_OF_SPADES, card2=FIVE_OF_DIAMONDS)
FOUR_TWO_OFF_SUIT = HoleCards(card1=FOUR_OF_SPADES, card2=TWO_OF_DIAMONDS)
THREE_TWO_OFF_SUIT = HoleCards(card1=THREE_OF_SPADES, card2=TWO_OF_DIAMONDS)


def test_pair_bonus():
    assert PAIR_OF_FIVES.summed_value > KING_QUEEN_SUITED.summed_value
    assert KING_QUEEN_SUITED.summed_value > PAIR_OF_FOURS.summed_value
    assert FIVE_FOUR_SUITED.summed_value > PAIR_OF_TWOS.summed_value
    assert PAIR_OF_TWOS.summed_value > KING_QUEEN_OFF_SUIT.summed_value
    assert PAIR_OF_TWOS.summed_value > FOUR_THREE_SUITED.summed_value


def test_flush_potential_bonus_not_too_high():
    assert ACE_QUEEN_OFF_SUIT.summed_value > ACE_JACK_SUITED.summed_value


def test_centrality_bonus_not_too_high():
    assert ACE_JACK_SUITED.summed_value > ACE_NINE_SUITED.summed_value


def test_straight_potential_bonus_not_too_high():
    assert SEVEN_TWO_OFF_SUIT.summed_value > SIX_FIVE_OFF_SUIT.summed_value


def test_obvious_dominance():
    assert FOUR_TWO_OFF_SUIT.summed_value > THREE_TWO_OFF_SUIT.summed_value


def test_pair_aces_match_constant():
    assert PAIR_OF_ACES.summed_value == VALUE_OF_POCKET_ACES_BEFORE_SHRINKING


def test_weakest_hand_in_top_50pct_matches_constant():
    assert (
        EIGHT_SEVEN_SUITED.summed_value
        == VALUE_OF_WEAKEST_HAND_STILL_IN_TOP_50PCT_OF_HANDS_BEFORE_SHRINKING
    )


def test_subtraction_factors_match():
    assert (
        SUBTRACTION_CONSTANT_AFTER_SHRINKING
        == OTHER_SUBTRACTION_CONSTANT_AFTER_SHRINKING
    )

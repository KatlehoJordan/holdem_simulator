from src.card import Card
from src.hole_cards import HoleCards
from src.rank import Rank
from src.scaling_constants import (
    OTHER_SUBTRACTION_CONSTANT_AFTER_SHRINKING,
    SUBTRACTION_CONSTANT_AFTER_SHRINKING,
    VALUE_OF_POCKET_ACES_BEFORE_SHRINKING,
    VALUE_OF_WEAKEST_HAND_STILL_IN_TOP_50PCT_OF_HANDS_BEFORE_SHRINKING,
)
from src.suit import Suit

ACE_OF_SPADES = Card(rank=Rank("Ace"), suit=Suit("Spades"))
ACE_OF_DIAMONDS = Card(rank=Rank("Ace"), suit=Suit("Diamonds"))
PAIR_OF_ACES = HoleCards(card1=ACE_OF_SPADES, card2=ACE_OF_DIAMONDS)

EIGHT_OF_SPADES = Card(rank=Rank("8"), suit=Suit("Spades"))
EIGHT_OF_DIAMONDS = Card(rank=Rank("8"), suit=Suit("Diamonds"))
PAIR_OF_EIGHTS = HoleCards(card1=EIGHT_OF_SPADES, card2=EIGHT_OF_DIAMONDS)

QUEEN_OF_DIAMONDS = Card(rank=Rank("Queen"), suit=Suit("Diamonds"))
ACE_QUEEN_OFF_SUIT = HoleCards(card1=ACE_OF_SPADES, card2=QUEEN_OF_DIAMONDS)

JACK_OF_SPADES = Card(rank=Rank("Jack"), suit=Suit("Spades"))
ACE_JACK_SUITED = HoleCards(card1=ACE_OF_SPADES, card2=JACK_OF_SPADES)

TEN_OF_DIAMONDS = Card(rank=Rank("10"), suit=Suit("Diamonds"))
ACE_TEN_OFF_SUIT = HoleCards(card1=ACE_OF_SPADES, card2=TEN_OF_DIAMONDS)

NINE_OF_SPADES = Card(rank=Rank("9"), suit=Suit("Spades"))
ACE_NINE_SUITED = HoleCards(card1=ACE_OF_SPADES, card2=NINE_OF_SPADES)

TWO_OF_SPADES = Card(rank=Rank("2"), suit=Suit("Spades"))
TWO_OF_DIAMONDS = Card(rank=Rank("2"), suit=Suit("Diamonds"))
PAIR_OF_TWOS = HoleCards(card1=TWO_OF_SPADES, card2=TWO_OF_DIAMONDS)

SEVEN_OF_SPADES = Card(rank=Rank("7"), suit=Suit("Spades"))
EIGHT_SEVEN_SUITED = HoleCards(card1=EIGHT_OF_SPADES, card2=SEVEN_OF_SPADES)

SEVEN_TWO_OFF_SUIT = HoleCards(card1=SEVEN_OF_SPADES, card2=TWO_OF_DIAMONDS)

SIX_OF_SPADES = Card(rank=Rank("6"), suit=Suit("Spades"))
FIVE_OF_DIAMONDS = Card(rank=Rank("5"), suit=Suit("Diamonds"))
SIX_FIVE_OFF_SUIT = HoleCards(card1=SIX_OF_SPADES, card2=FIVE_OF_DIAMONDS)

FIVE_OF_SPADES = Card(rank=Rank("5"), suit=Suit("Spades"))
FOUR_OF_SPADES = Card(rank=Rank("4"), suit=Suit("Spades"))
FIVE_FOUR_SUITED = HoleCards(card1=FIVE_OF_SPADES, card2=FOUR_OF_SPADES)

FOUR_TWO_OFF_SUIT = HoleCards(card1=FOUR_OF_SPADES, card2=TWO_OF_DIAMONDS)

THREE_OF_SPADES = Card(rank=Rank("3"), suit=Suit("Spades"))
FOUR_THREE_SUITED = HoleCards(card1=FOUR_OF_SPADES, card2=THREE_OF_SPADES)

THREE_OF_SPADES = Card(rank=Rank("3"), suit=Suit("Spades"))
THREE_TWO_OFF_SUIT = HoleCards(card1=THREE_OF_SPADES, card2=TWO_OF_DIAMONDS)


def test_pair_bonus():
    assert PAIR_OF_EIGHTS.summed_value > ACE_QUEEN_OFF_SUIT.summed_value
    assert FIVE_FOUR_SUITED.summed_value > PAIR_OF_TWOS.summed_value
    assert PAIR_OF_TWOS.summed_value > ACE_TEN_OFF_SUIT.summed_value
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

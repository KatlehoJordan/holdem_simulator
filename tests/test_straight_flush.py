import pytest

from src.community_cards import CommunityCards
from src.deck import Deck
from src.hole_cards import HoleCards
from src.player_hand import PlayerHand
from tests.tests_config import (
    ACE_OF_SPADES,
    EIGHT_OF_SPADES,
    FIVE_OF_DIAMONDS,
    FIVE_OF_SPADES,
    FOUR_OF_SPADES,
    JACK_OF_SPADES,
    KING_OF_SPADES,
    NINE_OF_SPADES,
    QUEEN_OF_SPADES,
    SEVEN_OF_SPADES,
    SIX_OF_SPADES,
    TEN_OF_SPADES,
    THREE_OF_SPADES,
    TWO_OF_SPADES,
)

HOLE_CARDS = HoleCards(deck=Deck(), card1=TWO_OF_SPADES, card2=THREE_OF_SPADES)

STRAIGHT_FLUSH_LOW = CommunityCards(
    deck=Deck(),
    card1=FOUR_OF_SPADES,
    card2=FIVE_OF_SPADES,
    card3=NINE_OF_SPADES,
    card4=TEN_OF_SPADES,
    card5=ACE_OF_SPADES,
)

STRAIGHT_FLUSH_MED = CommunityCards(
    deck=Deck(),
    card1=FIVE_OF_SPADES,
    card2=SIX_OF_SPADES,
    card3=SEVEN_OF_SPADES,
    card4=EIGHT_OF_SPADES,
    card5=NINE_OF_SPADES,
)

STRAIGHT_FLUSH_HI = CommunityCards(
    deck=Deck(),
    card1=TEN_OF_SPADES,
    card2=JACK_OF_SPADES,
    card3=QUEEN_OF_SPADES,
    card4=KING_OF_SPADES,
    card5=ACE_OF_SPADES,
)

STRAIGHT_NO_FLUSH = CommunityCards(
    deck=Deck(),
    card1=FOUR_OF_SPADES,
    card2=FIVE_OF_DIAMONDS,
    card3=NINE_OF_SPADES,
    card4=TEN_OF_SPADES,
    card5=ACE_OF_SPADES,
)

FLUSH_NO_STRAIGHT = CommunityCards(
    deck=Deck(),
    card1=FOUR_OF_SPADES,
    card2=FIVE_OF_SPADES,
    card3=SEVEN_OF_SPADES,
    card4=EIGHT_OF_SPADES,
    card5=NINE_OF_SPADES,
)

NO_FLUSH_NOR_STRAIGHT = CommunityCards(
    deck=Deck(),
    card1=FOUR_OF_SPADES,
    card2=FIVE_OF_DIAMONDS,
    card3=SEVEN_OF_SPADES,
    card4=EIGHT_OF_SPADES,
    card5=NINE_OF_SPADES,
)


def test_validate_straight_flush():
    assert PlayerHand(hole_cards=HOLE_CARDS, community_cards=STRAIGHT_FLUSH_LOW)
    assert PlayerHand(hole_cards=HOLE_CARDS, community_cards=STRAIGHT_FLUSH_MED)
    assert PlayerHand(hole_cards=HOLE_CARDS, community_cards=STRAIGHT_FLUSH_HI)

    with pytest.raises(ValueError):
        PlayerHand(hole_cards=HOLE_CARDS, community_cards=STRAIGHT_NO_FLUSH)
    with pytest.raises(ValueError):
        PlayerHand(hole_cards=HOLE_CARDS, community_cards=FLUSH_NO_STRAIGHT)
    with pytest.raises(ValueError):
        PlayerHand(hole_cards=HOLE_CARDS, community_cards=NO_FLUSH_NOR_STRAIGHT)

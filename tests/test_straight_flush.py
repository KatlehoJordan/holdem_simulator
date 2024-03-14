import pytest

from src.community_cards import CommunityCards
from src.deck import Deck
from src.hole_cards import HoleCards
from src.player_hand import PlayerHand
from src.straight_flush import StraightFlush
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

STRAIGHT_FLUSH_MULTIPLE = CommunityCards(
    deck=Deck(),
    card1=FOUR_OF_SPADES,
    card2=FIVE_OF_SPADES,
    card3=SIX_OF_SPADES,
    card4=SEVEN_OF_SPADES,
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
    test_cases = [
        (STRAIGHT_FLUSH_LOW, True),
        (STRAIGHT_FLUSH_MULTIPLE, True),
        (STRAIGHT_FLUSH_MED, True),
        (STRAIGHT_FLUSH_HI, True),
        (STRAIGHT_NO_FLUSH, False),
        (FLUSH_NO_STRAIGHT, False),
        (NO_FLUSH_NOR_STRAIGHT, False),
    ]

    for community_cards, expected in test_cases:
        assert (
            isinstance(
                PlayerHand(
                    hole_cards=HOLE_CARDS, community_cards=community_cards
                ).hand_type,
                StraightFlush,
            )
            is expected
        )


def test_straight_flush_winners():
    straight_flush_low = PlayerHand(
        hole_cards=HOLE_CARDS, community_cards=STRAIGHT_FLUSH_LOW
    ).hand_type
    straight_flush_multiple = PlayerHand(
        hole_cards=HOLE_CARDS, community_cards=STRAIGHT_FLUSH_MULTIPLE
    ).hand_type
    straight_flush_med = PlayerHand(
        hole_cards=HOLE_CARDS, community_cards=STRAIGHT_FLUSH_MED
    ).hand_type
    straight_flush_hi = PlayerHand(
        hole_cards=HOLE_CARDS, community_cards=STRAIGHT_FLUSH_HI
    ).hand_type
    # TODO: Remove type: ignore comments after full implementation in player_hand
    hand_type_scores = [
        straight_flush_low.hand_type_score,  # type: ignore
        straight_flush_multiple.hand_type_score,  # type: ignore
        straight_flush_med.hand_type_score,  # type: ignore
        straight_flush_hi.hand_type_score,  # type: ignore
    ]

    assert all(score == hand_type_scores[0] for score in hand_type_scores)

    top_ranks = [
        straight_flush_low.top_ranks[~0],  # type: ignore
        straight_flush_multiple.top_ranks[~0],  # type: ignore
        straight_flush_med.top_ranks[~0],  # type: ignore
        straight_flush_hi.top_ranks[~0],  # type: ignore
    ]

    assert top_ranks == sorted(top_ranks)

from tkinter import FIRST

from src.config import logger
from src.hand import HAND_TIE_FLAVOR, _determine_winners_and_losers
from src.player_hand import (
    FIRST_PLAYER_WINS_STRING,
    PLAYERS_TIE_STRING,
    PlayerHand,
    compare_player_hands,
)
from tests.tests_config import (
    make_community_cards_for_testing,
    make_hole_cards_for_testing,
)

"""
Regression tests for previously identified issues.

These tests are for cases where the logic was previously incorrect and has since been fixed.

The naming convention for these tests is as follows:
- case_<issue_number>: The issue number is incremented as new regression tests are built.
"""

CASE_001_COMMUNITY_SPADES_FLUSH_10_HI = make_community_cards_for_testing(
    [
        "6_OF_SPADES",
        "2_OF_SPADES",
        "9_OF_SPADES",
        "10_OF_SPADES",
        "7_OF_SPADES",
    ]
)

CASE_001_YOUR_HOLE_CARDS = make_hole_cards_for_testing(
    [
        "ACE_OF_DIAMONDS",
        "JACK_OF_SPADES",
    ]
)

CASE_002_COMMUNITY_STRAIGHT_QUEEN_HIGH = make_community_cards_for_testing(
    [
        "JACK_OF_DIAMONDS",
        "9_OF_HEARTS",
        "10_OF_SPADES",
        "8_OF_DIAMONDS",
        "5_OF_DIAMONDS",
    ]
)

CASE_002_PLAYER_1_HOLE_CARDS = make_hole_cards_for_testing(
    [
        "QUEEN_OF_HEARTS",
        "QUEEN_OF_SPADES",
    ]
)

CASE_002_PLAYER_2_HOLE_CARDS = make_hole_cards_for_testing(
    [
        "QUEEN_OF_CLUBS",
        "6_OF_DIAMONDS",
    ]
)


CASE_003_COMMUNITY_STRAIGHT_QUEEN_HIGH = make_community_cards_for_testing(
    [
        "6_OF_HEARTS",
        "ACE_OF_SPADES",
        "4_OF_HEARTS",
        "7_OF_DIAMONDS",
        "8_OF_CLUBS",
    ]
)

CASE_003_PLAYER_1_HOLE_CARDS = make_hole_cards_for_testing(
    [
        "10_OF_DIAMONDS",
        "9_OF_CLUBS",
    ]
)

CASE_003_PLAYER_2_HOLE_CARDS = make_hole_cards_for_testing(
    [
        "5_OF_CLUBS",
        "2_OF_CLUBS",
    ]
)

CASE_004_TIE_WINNING_TYPE_WITH_3_PLAYERS = make_community_cards_for_testing(
    [
        "7_OF_DIAMONDS",
        "KING_OF_CLUBS",
        "6_OF_SPADES",
        "3_OF_HEARTS",
        "KING_OF_HEARTS",
    ]
)

CASE_004_PLAYER_1_HOLE_CARDS = make_hole_cards_for_testing(
    [
        "6_OF_CLUBS",
        "2_OF_CLUBS",
    ]
)

CASE_004_PLAYER_2_HOLE_CARDS = make_hole_cards_for_testing(
    [
        "6_OF_HEARTS",
        "5_OF_SPADES",
    ]
)

CASE_004_PLAYER_3_HOLE_CARDS = make_hole_cards_for_testing(
    [
        "ACE_OF_SPADES",
        "5_OF_HEARTS",
    ]
)

CASE_005_TIE_WINNING_TYPE_WITH_3_PLAYERS = make_community_cards_for_testing(
    [
        "6_OF_DIAMONDS",
        "QUEEN_OF_DIAMONDS",
        "8_OF_CLUBS",
        "5_OF_HEARTS",
        "4_OF_CLUBS",
    ]
)

CASE_005_PLAYER_1_HOLE_CARDS = make_hole_cards_for_testing(
    [
        "7_OF_CLUBS",
        "6_OF_SPADES",
    ]
)

CASE_005_PLAYER_2_HOLE_CARDS = make_hole_cards_for_testing(
    [
        "ACE_OF_DIAMONDS",
        "7_OF_HEARTS",
    ]
)

CASE_005_PLAYER_3_HOLE_CARDS = make_hole_cards_for_testing(
    [
        "8_OF_DIAMONDS",
        "7_OF_DIAMONDS",
    ]
)


def test_case_001():
    logger.debug(
        "Previously, the the winning hand was identified as a 10-high flush, but this is a Jack-high flush. This was due to incorrect sorting of the flush cards by rank value."
    )
    player_hand = PlayerHand(
        hole_cards=CASE_001_YOUR_HOLE_CARDS,
        community_cards=CASE_001_COMMUNITY_SPADES_FLUSH_10_HI,
    )
    assert player_hand.hand_type.name == "Flush: Jack, 10, 9, 7, 6, in Spades."


def test_case_002():
    logger.debug(
        "Previously, two straights with these cards mistakenly identified the first player as the winner. This was due to incorrect sorting of the top-ranked cards in the straight."
    )
    community_cards = CASE_002_COMMUNITY_STRAIGHT_QUEEN_HIGH
    player_hand_1 = PlayerHand(
        hole_cards=CASE_002_PLAYER_1_HOLE_CARDS,
        community_cards=community_cards,
    )
    player_hand_2 = PlayerHand(
        hole_cards=CASE_002_PLAYER_2_HOLE_CARDS,
        community_cards=community_cards,
    )
    assert compare_player_hands(player_hand_1, player_hand_2) == PLAYERS_TIE_STRING


def test_case_003():
    logger.debug(
        "Previously, the winning hand was incorrectly identified as an Ace-high straight. The winner is actually a 10-high straight. There is also a 8-high straight that is a loser. This was due to incorrect sorting of the top-ranked cards in the straight."
    )
    community_cards = CASE_003_COMMUNITY_STRAIGHT_QUEEN_HIGH
    player_hand_1 = PlayerHand(
        hole_cards=CASE_003_PLAYER_1_HOLE_CARDS,
        community_cards=community_cards,
    )
    player_hand_2 = PlayerHand(
        hole_cards=CASE_003_PLAYER_2_HOLE_CARDS,
        community_cards=community_cards,
    )
    assert (
        compare_player_hands(player_hand_1, player_hand_2) == FIRST_PLAYER_WINS_STRING
    )
    assert player_hand_1.hand_type.name == "Straight: 10 high."
    assert player_hand_2.hand_type.name == "Straight: 8 high."


def test_case_004():
    logger.debug(
        "Previously, the winning type was identified as 'Single winner' though there is a tie between player 1 and player 2. This was due to compare_player_hands not being able to compare more than two players at a time before and it's implementation in hand.py was not always returning a 'tie' if the final two hands compared were not a tie although other hands were tied."
    )
    community_cards = CASE_004_TIE_WINNING_TYPE_WITH_3_PLAYERS
    player_hand_1 = PlayerHand(
        hole_cards=CASE_004_PLAYER_1_HOLE_CARDS,
        community_cards=community_cards,
    )
    player_hand_2 = PlayerHand(
        hole_cards=CASE_004_PLAYER_2_HOLE_CARDS,
        community_cards=community_cards,
    )
    player_hand_3 = PlayerHand(
        hole_cards=CASE_004_PLAYER_3_HOLE_CARDS,
        community_cards=community_cards,
    )
    assert (
        compare_player_hands(player_hand_1, player_hand_2, player_hand_3)
        == PLAYERS_TIE_STRING
    )


def test_case_005():
    logger.debug(
        "Previously, only 2 winners were counted, but all 3 players have the same 8-high straight and should therefore be counted. This was due to poor control flow in the determine_winners_and_losers function."
    )
    community_cards = CASE_005_TIE_WINNING_TYPE_WITH_3_PLAYERS
    player_hand_1 = PlayerHand(
        hole_cards=CASE_005_PLAYER_1_HOLE_CARDS,
        community_cards=community_cards,
    )
    player_hand_2 = PlayerHand(
        hole_cards=CASE_005_PLAYER_2_HOLE_CARDS,
        community_cards=community_cards,
    )
    player_hand_3 = PlayerHand(
        hole_cards=CASE_005_PLAYER_3_HOLE_CARDS,
        community_cards=community_cards,
    )
    player_hands_in_the_hand = [player_hand_1, player_hand_2, player_hand_3]
    (
        winning_type,
        winning_hands,
        losing_hands,
        winning_hole_cards_flavors,
        losing_hole_cards_flavors,
    ) = _determine_winners_and_losers(
        player_hands_in_the_hand,
    )
    assert winning_type == HAND_TIE_FLAVOR
    assert len(winning_hands) == 3
    assert len(losing_hands) == 0
    assert len(winning_hole_cards_flavors) == 3
    assert len(losing_hole_cards_flavors) == 0

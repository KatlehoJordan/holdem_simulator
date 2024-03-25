from src.config import logger
from src.player_hand import (
    assert_tie_regardless_of_order,
    assert_winner_regardless_of_order,
)
from src.straight import STRAIGHT_HAND_TYPE_SCORE
from tests.test_flush import HOLE_CARDS_4_5_HEARTS, POCKET_4S
from tests.test_straight_flush import (
    HOLE_CARDS_2_7_SPADES_DIAMONDS,
    HOLE_CARDS_6_7_DIAMONDS,
    HOLE_CARDS_KING_9_CLUBS,
    POCKET_ACES,
)
from tests.tests_config import (
    HOLE_CARDS_2_3_SPADES,
    hand_type_test_builder,
    make_community_cards_for_testing,
    make_hole_cards_for_testing,
)

STRAIGHT_5_HI = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "5_OF_DIAMONDS",
        "9_OF_DIAMONDS",
        "10_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

STRAIGHT_5_HI_ALTERNATE = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "5_OF_DIAMONDS",
        "9_OF_DIAMONDS",
        "10_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

STRAIGHT_6_HI = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "5_OF_DIAMONDS",
        "6_OF_DIAMONDS",
        "10_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

VALID_STRAIGHT_CASES_IN_ASCENDING_ORDER = [
    STRAIGHT_5_HI,
    STRAIGHT_5_HI_ALTERNATE,
    STRAIGHT_6_HI,
]

COMMUNITY_STRAIGHT_10_HI = make_community_cards_for_testing(
    [
        "6_OF_HEARTS",
        "7_OF_CLUBS",
        "8_OF_SPADES",
        "9_OF_DIAMONDS",
        "10_OF_HEARTS",
    ]
)

HOLE_CARDS_10_JACK_SPADES = make_hole_cards_for_testing(
    [
        "10_OF_SPADES",
        "JACK_OF_SPADES",
    ]
)

STRAIGHT_DOMINATING_WEAKER_HANDS = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "5_OF_CLUBS",
        "8_OF_SPADES",
        "9_OF_HEARTS",
        "ACE_OF_SPADES",
    ]
)


def test_straight():
    hand_type_test_builder(
        hand_tested="straight",
        valid_cases_in_ascending_strength=VALID_STRAIGHT_CASES_IN_ASCENDING_ORDER,
        expected_hand_type_score=STRAIGHT_HAND_TYPE_SCORE,
        valid_tie_case_1=STRAIGHT_5_HI,
        valid_tie_case_2=STRAIGHT_5_HI_ALTERNATE,
    )


def test_compare_straights():
    logger.debug("Test that the stronger straight is always the winner")
    assert_winner_regardless_of_order(
        community_cards=COMMUNITY_STRAIGHT_10_HI,
        winning_hole_cards=HOLE_CARDS_10_JACK_SPADES,
        losing_hole_cards=HOLE_CARDS_2_3_SPADES,
    )


def test_community_straight_ties():
    logger.debug("Test that a community straight is always a tie")
    assert_tie_regardless_of_order(
        community_cards=COMMUNITY_STRAIGHT_10_HI,
        hole_cards_1=POCKET_ACES,
        hole_cards_2=HOLE_CARDS_2_3_SPADES,
    )


def test_compare_straight_to_other_hands():
    logger.debug("Test that a straight beats a three of a kind")
    assert_winner_regardless_of_order(
        community_cards=STRAIGHT_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=HOLE_CARDS_6_7_DIAMONDS,
        losing_hole_cards=POCKET_4S,
    )

    logger.debug("Test that a straight beats a two pair")
    assert_winner_regardless_of_order(
        community_cards=STRAIGHT_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=HOLE_CARDS_6_7_DIAMONDS,
        losing_hole_cards=HOLE_CARDS_4_5_HEARTS,
    )

    logger.debug("Test that a straight beats a pair")
    assert_winner_regardless_of_order(
        community_cards=STRAIGHT_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=HOLE_CARDS_6_7_DIAMONDS,
        losing_hole_cards=HOLE_CARDS_KING_9_CLUBS,
    )

    logger.debug("Test that a straight beats a high card")
    assert_winner_regardless_of_order(
        community_cards=STRAIGHT_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=HOLE_CARDS_6_7_DIAMONDS,
        losing_hole_cards=HOLE_CARDS_2_7_SPADES_DIAMONDS,
    )

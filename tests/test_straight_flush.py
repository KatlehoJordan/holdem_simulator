from src.config import logger
from src.player_hand import (
    assert_tie_regardless_of_order,
    assert_winner_regardless_of_order,
)
from src.straight_flush import STRAIGHT_FLUSH_HAND_TYPE_SCORE
from tests.tests_config import (
    HOLE_CARDS_2_3_SPADES,
    hand_type_test_builder,
    make_community_cards_for_testing,
    make_hole_cards_for_testing,
)

STRAIGHT_FLUSH_5_HI_SPADES = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "5_OF_SPADES",
        "9_OF_SPADES",
        "10_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

STRAIGHT_FLUSH_5_HI_SPADES_ALTERNATE = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "5_OF_SPADES",
        "8_OF_SPADES",
        "9_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

STRAIGHT_FLUSH_7_HI_SPADES = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "5_OF_SPADES",
        "6_OF_SPADES",
        "7_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

STRAIGHT_FLUSH_9_HI_SPADES = make_community_cards_for_testing(
    [
        "5_OF_SPADES",
        "6_OF_SPADES",
        "7_OF_SPADES",
        "8_OF_SPADES",
        "9_OF_SPADES",
    ]
)

COMMUNITY_ROYAL_FLUSH = make_community_cards_for_testing(
    [
        "10_OF_SPADES",
        "JACK_OF_SPADES",
        "QUEEN_OF_SPADES",
        "KING_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

VALID_STRAIGHT_FLUSH_CASES_WITH_2_3_SPADES_HOLE_CARDS_IN_ASCENDING_STRENGTH = [
    STRAIGHT_FLUSH_5_HI_SPADES,
    STRAIGHT_FLUSH_5_HI_SPADES_ALTERNATE,
    STRAIGHT_FLUSH_7_HI_SPADES,
    STRAIGHT_FLUSH_9_HI_SPADES,
    COMMUNITY_ROYAL_FLUSH,
]


STRAIGHT_FLUSH_9_OR_5_HI_SPADES = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "5_OF_SPADES",
        "6_OF_SPADES",
        "7_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

HOLE_CARDS_8_9_SPADES = make_hole_cards_for_testing(
    [
        "8_OF_SPADES",
        "9_OF_SPADES",
    ]
)

STRAIGHT_FLUSH_DOMINATING_ALL_OTHERS = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "5_OF_SPADES",
        "9_OF_SPADES",
        "9_OF_HEARTS",
        "ACE_OF_SPADES",
    ]
)

POCKET_9S = make_hole_cards_for_testing(
    [
        "9_OF_CLUBS",
        "9_OF_DIAMONDS",
    ]
)

POCKET_ACES = make_hole_cards_for_testing(
    [
        "ACE_OF_CLUBS",
        "ACE_OF_DIAMONDS",
    ]
)

HOLE_CARDS_KING_QUEEN_SPADES = make_hole_cards_for_testing(
    [
        "KING_OF_SPADES",
        "QUEEN_OF_SPADES",
    ]
)

HOLE_CARDS_2_3_HEARTS = make_hole_cards_for_testing(
    [
        "2_OF_HEARTS",
        "3_OF_HEARTS",
    ]
)

HOLE_CARDS_KING_9_CLUBS = make_hole_cards_for_testing(
    [
        "KING_OF_CLUBS",
        "9_OF_CLUBS",
    ]
)

HOLE_CARDS_ACE_KING_HEARTS = make_hole_cards_for_testing(
    [
        "ACE_OF_HEARTS",
        "KING_OF_HEARTS",
    ]
)

HOLE_CARDS_6_7_DIAMONDS = make_hole_cards_for_testing(
    [
        "6_OF_DIAMONDS",
        "7_OF_DIAMONDS",
    ]
)


def test_straight_flush():
    hand_type_test_builder(
        hand_tested="straight flush",
        valid_cases_in_ascending_strength=VALID_STRAIGHT_FLUSH_CASES_WITH_2_3_SPADES_HOLE_CARDS_IN_ASCENDING_STRENGTH,
        expected_hand_type_score=STRAIGHT_FLUSH_HAND_TYPE_SCORE,
        valid_tie_case_1=STRAIGHT_FLUSH_5_HI_SPADES,
        valid_tie_case_2=STRAIGHT_FLUSH_5_HI_SPADES_ALTERNATE,
    )


def test_compare_straight_flushes():
    logger.debug("Test that the stronger straight flush is always the winner")
    assert_winner_regardless_of_order(
        community_cards=STRAIGHT_FLUSH_9_OR_5_HI_SPADES,
        winning_hole_cards=HOLE_CARDS_8_9_SPADES,
        losing_hole_cards=HOLE_CARDS_2_3_SPADES,
    )


def test_community_royal_flush_ties():
    logger.debug("Test that a community royal flush is always a tie")
    assert_tie_regardless_of_order(
        community_cards=COMMUNITY_ROYAL_FLUSH,
        hole_cards_1=HOLE_CARDS_2_3_SPADES,
        hole_cards_2=POCKET_9S,
    )


def test_compare_straight_flush_to_other_hands():
    logger.debug("Test that a straight flush beats a four of a kind")
    assert_winner_regardless_of_order(
        community_cards=STRAIGHT_FLUSH_DOMINATING_ALL_OTHERS,
        winning_hole_cards=HOLE_CARDS_2_3_SPADES,
        losing_hole_cards=POCKET_9S,
    )

    logger.debug("Test that a straight flush beats a full house")
    assert_winner_regardless_of_order(
        community_cards=STRAIGHT_FLUSH_DOMINATING_ALL_OTHERS,
        winning_hole_cards=HOLE_CARDS_2_3_SPADES,
        losing_hole_cards=POCKET_ACES,
    )

    logger.debug("Test that a straight flush beats a flush")
    assert_winner_regardless_of_order(
        community_cards=STRAIGHT_FLUSH_DOMINATING_ALL_OTHERS,
        winning_hole_cards=HOLE_CARDS_2_3_SPADES,
        losing_hole_cards=HOLE_CARDS_KING_QUEEN_SPADES,
    )

    logger.debug("Test that a straight flush beats a straight")
    assert_winner_regardless_of_order(
        community_cards=STRAIGHT_FLUSH_DOMINATING_ALL_OTHERS,
        winning_hole_cards=HOLE_CARDS_2_3_SPADES,
        losing_hole_cards=HOLE_CARDS_2_3_HEARTS,
    )

    logger.debug("Test that a straight flush beats a three of a kind")
    assert_winner_regardless_of_order(
        community_cards=STRAIGHT_FLUSH_DOMINATING_ALL_OTHERS,
        winning_hole_cards=HOLE_CARDS_2_3_SPADES,
        losing_hole_cards=HOLE_CARDS_KING_9_CLUBS,
    )

    logger.debug("Test that a straight flush beats a two pair")
    assert_winner_regardless_of_order(
        community_cards=STRAIGHT_FLUSH_DOMINATING_ALL_OTHERS,
        winning_hole_cards=HOLE_CARDS_2_3_SPADES,
        losing_hole_cards=HOLE_CARDS_ACE_KING_HEARTS,
    )

    logger.debug("Test that a straight flush beats a pair")
    assert_winner_regardless_of_order(
        community_cards=STRAIGHT_FLUSH_DOMINATING_ALL_OTHERS,
        winning_hole_cards=HOLE_CARDS_2_3_SPADES,
        losing_hole_cards=HOLE_CARDS_6_7_DIAMONDS,
    )

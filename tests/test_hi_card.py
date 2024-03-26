from src.config import logger
from src.hi_card import HI_CARD_HAND_TYPE_SCORE
from src.player_hand import (
    assert_tie_regardless_of_order,
    assert_winner_regardless_of_order,
)
from tests.test_straight_flush import (
    HOLE_CARDS_2_7_SPADES_DIAMONDS,
    HOLE_CARDS_KING_9_CLUBS,
)
from tests.tests_config import (
    HOLE_CARDS_2_3_SPADES,
    hand_type_test_builder,
    make_community_cards_for_testing,
    make_hole_cards_for_testing,
)

HI_CARD_9 = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "5_OF_DIAMONDS",
        "7_OF_DIAMONDS",
        "8_OF_SPADES",
        "9_OF_SPADES",
    ]
)

HI_CARD_10_9 = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "5_OF_DIAMONDS",
        "7_OF_DIAMONDS",
        "9_OF_SPADES",
        "10_OF_SPADES",
    ]
)

HI_CARD_10_8 = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "5_OF_DIAMONDS",
        "7_OF_DIAMONDS",
        "8_OF_SPADES",
        "10_OF_SPADES",
    ]
)

HI_CARD_10_8_ALTERNATE = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "5_OF_DIAMONDS",
        "7_OF_DIAMONDS",
        "8_OF_DIAMONDS",
        "10_OF_SPADES",
    ]
)

VALID_HI_CARD_CASES_IN_ASCENDING_ORDER = [
    HI_CARD_9,
    HI_CARD_10_8,
    HI_CARD_10_8_ALTERNATE,
    HI_CARD_10_9,
]

COMMUNITY_HI_CARD_ACE = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "5_OF_CLUBS",
        "8_OF_HEARTS",
        "10_OF_HEARTS",
        "ACE_OF_SPADES",
    ]
)

HOLE_CARDS_2_3_CLUBS = make_hole_cards_for_testing(
    [
        "2_OF_CLUBS",
        "3_OF_CLUBS",
    ]
)


def test_hi_card():
    hand_type_test_builder(
        hand_tested="hi card",
        valid_cases_in_ascending_strength=VALID_HI_CARD_CASES_IN_ASCENDING_ORDER,
        expected_hand_type_score=HI_CARD_HAND_TYPE_SCORE,
        valid_tie_case_1=HI_CARD_10_8,
        valid_tie_case_2=HI_CARD_10_8_ALTERNATE,
    )


def test_compare_hi_cards():
    logger.debug("Test that the stronger hi card hand is always the winner")
    assert_winner_regardless_of_order(
        community_cards=COMMUNITY_HI_CARD_ACE,
        winning_hole_cards=HOLE_CARDS_KING_9_CLUBS,
        losing_hole_cards=HOLE_CARDS_2_7_SPADES_DIAMONDS,
    )


def test_community_hi_card_ties():
    logger.debug("Test that a community hi card hand is always a tie")
    assert_tie_regardless_of_order(
        community_cards=COMMUNITY_HI_CARD_ACE,
        hole_cards_1=HOLE_CARDS_2_3_SPADES,
        hole_cards_2=HOLE_CARDS_2_3_CLUBS,
    )

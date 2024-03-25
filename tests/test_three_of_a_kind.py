from src.config import logger
from src.player_hand import (
    assert_tie_regardless_of_order,
    assert_winner_regardless_of_order,
)
from src.three_of_a_kind import THREE_OF_A_KIND_HAND_TYPE_SCORE
from tests.test_flush import HOLE_CARDS_4_5_HEARTS
from tests.test_four_of_a_kind import POCKET_6S
from tests.test_straight_flush import (
    HOLE_CARDS_2_3_HEARTS,
    HOLE_CARDS_KING_9_CLUBS,
    HOLE_CARDS_KING_QUEEN_SPADES,
)
from tests.tests_config import (
    HOLE_CARDS_2_3_SPADES,
    hand_type_test_builder,
    make_community_cards_for_testing,
)

THREE_OF_A_KIND_2S = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "2_OF_HEARTS",
        "4_OF_SPADES",
        "7_OF_DIAMONDS",
        "ACE_OF_SPADES",
    ]
)

THREE_OF_A_KIND_2S_ALTERNATE = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "2_OF_CLUBS",
        "4_OF_SPADES",
        "7_OF_DIAMONDS",
        "ACE_OF_DIAMONDS",
    ]
)

THREE_OF_A_KIND_2S_WEAKER_KICKERS = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "2_OF_HEARTS",
        "4_OF_SPADES",
        "7_OF_DIAMONDS",
        "KING_OF_SPADES",
    ]
)

THREE_OF_A_KIND_2S_WEAKEST_KICKERS = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "2_OF_HEARTS",
        "4_OF_SPADES",
        "6_OF_DIAMONDS",
        "KING_OF_SPADES",
    ]
)

THREE_OF_A_KIND_3S = make_community_cards_for_testing(
    [
        "3_OF_DIAMONDS",
        "3_OF_HEARTS",
        "4_OF_SPADES",
        "7_OF_DIAMONDS",
        "ACE_OF_SPADES",
    ]
)

THREE_OF_A_KIND_4S = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "4_OF_HEARTS",
        "4_OF_CLUBS",
        "7_OF_DIAMONDS",
        "ACE_OF_SPADES",
    ]
)

COMMUNITY_THREE_OF_A_KIND_ACES = make_community_cards_for_testing(
    [
        "ACE_OF_DIAMONDS",
        "ACE_OF_HEARTS",
        "ACE_OF_CLUBS",
        "7_OF_DIAMONDS",
        "4_OF_SPADES",
    ]
)

VALID_THREE_OF_A_KIND_CASES_IN_ASCENDING_STRENGTH = [
    THREE_OF_A_KIND_2S_WEAKEST_KICKERS,
    THREE_OF_A_KIND_2S_WEAKER_KICKERS,
    THREE_OF_A_KIND_2S,
    THREE_OF_A_KIND_2S_ALTERNATE,
    THREE_OF_A_KIND_3S,
    THREE_OF_A_KIND_4S,
    COMMUNITY_THREE_OF_A_KIND_ACES,
]

THREE_OF_A_KIND_DOMINATING_WEAKER_HANDS = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "5_OF_CLUBS",
        "6_OF_HEARTS",
        "9_OF_HEARTS",
        "ACE_OF_SPADES",
    ]
)


def test_three_of_a_kind():
    hand_type_test_builder(
        hand_tested="three of a kind",
        valid_cases_in_ascending_strength=VALID_THREE_OF_A_KIND_CASES_IN_ASCENDING_STRENGTH,
        expected_hand_type_score=THREE_OF_A_KIND_HAND_TYPE_SCORE,
        valid_tie_case_1=THREE_OF_A_KIND_2S,
        valid_tie_case_2=THREE_OF_A_KIND_2S_ALTERNATE,
    )


def test_compare_three_of_a_kinds():
    logger.debug("Test that the stronger three of a kind is always the winner")
    assert_winner_regardless_of_order(
        community_cards=COMMUNITY_THREE_OF_A_KIND_ACES,
        winning_hole_cards=HOLE_CARDS_KING_QUEEN_SPADES,
        losing_hole_cards=HOLE_CARDS_KING_9_CLUBS,
    )


def test_community_three_of_a_kind_ties():
    logger.debug("Test that a community three of a kind is always a tie")
    assert_tie_regardless_of_order(
        community_cards=COMMUNITY_THREE_OF_A_KIND_ACES,
        hole_cards_1=HOLE_CARDS_2_3_HEARTS,
        hole_cards_2=HOLE_CARDS_2_3_SPADES,
    )


def test_compare_three_of_a_kind_to_other_hands():
    logger.debug("Test that a three of a kind beats a two pair")
    assert_winner_regardless_of_order(
        community_cards=THREE_OF_A_KIND_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=POCKET_6S,
        losing_hole_cards=HOLE_CARDS_4_5_HEARTS,
    )

    logger.debug("Test that a three of a kind beats a pair")
    assert_winner_regardless_of_order(
        community_cards=THREE_OF_A_KIND_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=POCKET_6S,
        losing_hole_cards=HOLE_CARDS_KING_9_CLUBS,
    )

    logger.debug("Test that a three of a kind beats a high card")
    assert_winner_regardless_of_order(
        community_cards=THREE_OF_A_KIND_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=POCKET_6S,
        losing_hole_cards=HOLE_CARDS_KING_QUEEN_SPADES,
    )

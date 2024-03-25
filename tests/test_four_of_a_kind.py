from src.config import logger
from src.four_of_a_kind import FOUR_OF_A_KIND_HAND_TYPE_SCORE
from src.player_hand import (
    assert_tie_regardless_of_order,
    assert_winner_regardless_of_order,
)
from tests.test_straight_flush import (
    HOLE_CARDS_2_3_HEARTS,
    HOLE_CARDS_6_7_DIAMONDS,
    HOLE_CARDS_ACE_KING_HEARTS,
    HOLE_CARDS_KING_9_CLUBS,
    HOLE_CARDS_KING_QUEEN_SPADES,
    POCKET_9S,
    POCKET_ACES,
)
from tests.tests_config import (
    hand_type_test_builder,
    make_community_cards_for_testing,
    make_hole_cards_for_testing,
)

FOUR_OF_A_KIND_2S = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "2_OF_HEARTS",
        "2_OF_CLUBS",
        "4_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

FOUR_OF_A_KIND_2S_ALTERNATE = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "2_OF_HEARTS",
        "2_OF_CLUBS",
        "5_OF_SPADES",
        "ACE_OF_DIAMONDS",
    ]
)

FOUR_OF_A_KIND_2S_WEAK_KICKERS = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "2_OF_HEARTS",
        "2_OF_CLUBS",
        "4_OF_SPADES",
        "4_OF_DIAMONDS",
    ]
)

FOUR_OF_A_KIND_3S = make_community_cards_for_testing(
    [
        "3_OF_DIAMONDS",
        "3_OF_HEARTS",
        "3_OF_CLUBS",
        "4_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

FOUR_OF_A_KIND_4S = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "4_OF_HEARTS",
        "4_OF_CLUBS",
        "4_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

FOUR_OF_A_KIND_ACES = make_community_cards_for_testing(
    [
        "ACE_OF_DIAMONDS",
        "ACE_OF_HEARTS",
        "ACE_OF_CLUBS",
        "ACE_OF_SPADES",
        "4_OF_SPADES",
    ]
)

VALID_FOUR_OF_A_KIND_CASES_IN_ASCENDING_STRENGTH = [
    FOUR_OF_A_KIND_2S_WEAK_KICKERS,
    FOUR_OF_A_KIND_2S,
    FOUR_OF_A_KIND_2S_ALTERNATE,
    FOUR_OF_A_KIND_3S,
    FOUR_OF_A_KIND_4S,
    FOUR_OF_A_KIND_ACES,
]

COMMUNITY_FOUR_OF_A_KIND_HOLE_KICKER = make_community_cards_for_testing(
    [
        "KING_OF_SPADES",
        "6_OF_DIAMONDS",
        "6_OF_SPADES",
        "6_OF_HEARTS",
        "6_OF_CLUBS",
    ]
)

COMMUNITY_FOUR_OF_A_KIND_AND_KICKER = make_community_cards_for_testing(
    [
        "ACE_OF_SPADES",
        "6_OF_DIAMONDS",
        "6_OF_SPADES",
        "6_OF_HEARTS",
        "6_OF_CLUBS",
    ]
)

FOUR_OF_A_KIND_DOMINATING_WEAKER_HANDS = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "5_OF_SPADES",
        "6_OF_HEARTS",
        "6_OF_CLUBS",
        "9_OF_SPADES",
    ]
)

POCKET_6S = make_hole_cards_for_testing(
    [
        "6_OF_DIAMONDS",
        "6_OF_SPADES",
    ]
)

FOUR_OF_A_KIND_DOMINATING_THREE_OF_A_KIND = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "5_OF_SPADES",
        "6_OF_HEARTS",
        "6_OF_CLUBS",
        "6_OF_SPADES",
    ]
)


def test_four_of_a_kind():
    hand_type_test_builder(
        hand_tested="four of a kind",
        valid_cases_in_ascending_strength=VALID_FOUR_OF_A_KIND_CASES_IN_ASCENDING_STRENGTH,
        expected_hand_type_score=FOUR_OF_A_KIND_HAND_TYPE_SCORE,
        valid_tie_case_1=FOUR_OF_A_KIND_2S,
        valid_tie_case_2=FOUR_OF_A_KIND_2S_ALTERNATE,
    )


def test_compare_four_of_a_kinds():
    logger.debug("Test that the stronger four of a kind is always the winner")
    assert_winner_regardless_of_order(
        community_cards=COMMUNITY_FOUR_OF_A_KIND_HOLE_KICKER,
        winning_hole_cards=HOLE_CARDS_ACE_KING_HEARTS,
        losing_hole_cards=HOLE_CARDS_KING_9_CLUBS,
    )


def test_community_four_of_a_kind_ties():
    logger.debug("Test that a community four of a kind with ace kicker is always a tie")
    assert_tie_regardless_of_order(
        community_cards=COMMUNITY_FOUR_OF_A_KIND_AND_KICKER,
        hole_cards_1=HOLE_CARDS_ACE_KING_HEARTS,
        hole_cards_2=HOLE_CARDS_KING_9_CLUBS,
    )
    assert_tie_regardless_of_order(
        community_cards=COMMUNITY_FOUR_OF_A_KIND_HOLE_KICKER,
        hole_cards_1=HOLE_CARDS_ACE_KING_HEARTS,
        hole_cards_2=POCKET_ACES,
    )


def test_compare_four_of_a_kind_to_other_hands():
    logger.debug("Test that a four of a kind beats a full house")
    assert_winner_regardless_of_order(
        community_cards=FOUR_OF_A_KIND_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=POCKET_6S,
        losing_hole_cards=POCKET_9S,
    )

    logger.debug("Test that a four of a kind beats a flush")
    assert_winner_regardless_of_order(
        community_cards=FOUR_OF_A_KIND_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=POCKET_6S,
        losing_hole_cards=HOLE_CARDS_KING_QUEEN_SPADES,
    )

    logger.debug("Test that a four of a kind beats a straight")
    assert_winner_regardless_of_order(
        community_cards=FOUR_OF_A_KIND_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=POCKET_6S,
        losing_hole_cards=HOLE_CARDS_2_3_HEARTS,
    )

    logger.debug("Test that a four of a kind beats a three of a kind")
    assert_winner_regardless_of_order(
        community_cards=FOUR_OF_A_KIND_DOMINATING_THREE_OF_A_KIND,
        winning_hole_cards=HOLE_CARDS_6_7_DIAMONDS,
        losing_hole_cards=HOLE_CARDS_KING_9_CLUBS,
    )

    logger.debug("Test that a four of a kind beats a two pair")
    assert_winner_regardless_of_order(
        community_cards=FOUR_OF_A_KIND_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=POCKET_6S,
        losing_hole_cards=HOLE_CARDS_KING_9_CLUBS,
    )

    logger.debug("Test that a four of a kind beats a pair")
    assert_winner_regardless_of_order(
        community_cards=FOUR_OF_A_KIND_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=POCKET_6S,
        losing_hole_cards=HOLE_CARDS_ACE_KING_HEARTS,
    )



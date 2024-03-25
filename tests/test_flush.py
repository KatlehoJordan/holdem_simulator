from src.config import logger
from src.flush import FLUSH_HAND_TYPE_SCORE
from src.player_hand import (
    assert_tie_regardless_of_order,
    assert_winner_regardless_of_order,
)
from tests.test_full_house import HOLE_CARDS_3_6_HEARTS
from tests.test_straight_flush import (
    HOLE_CARDS_KING_9_CLUBS,
    HOLE_CARDS_KING_QUEEN_SPADES,
    POCKET_9S,
    POCKET_ACES,
)
from tests.tests_config import (
    HOLE_CARDS_2_3_SPADES,
    hand_type_test_builder,
    make_community_cards_for_testing,
    make_hole_cards_for_testing,
)

COMMUNITY_FLUSH_9_HI_SPADES = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "5_OF_SPADES",
        "7_OF_SPADES",
        "8_OF_SPADES",
        "9_OF_SPADES",
    ]
)

FLUSH_9_HI_DIAMONDS = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "5_OF_DIAMONDS",
        "7_OF_DIAMONDS",
        "8_OF_DIAMONDS",
        "9_OF_DIAMONDS",
    ]
)

FLUSH_10_HI_SPADES = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "5_OF_SPADES",
        "7_OF_SPADES",
        "8_OF_SPADES",
        "10_OF_SPADES",
    ]
)

FLUSH_10_HI_SPADES_BETTER_KICKER = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "5_OF_SPADES",
        "7_OF_SPADES",
        "9_OF_SPADES",
        "10_OF_SPADES",
    ]
)

VALID_FLUSH_CASES_IN_ASCENDING_ORDER = [
    COMMUNITY_FLUSH_9_HI_SPADES,
    FLUSH_9_HI_DIAMONDS,
    FLUSH_10_HI_SPADES,
    FLUSH_10_HI_SPADES_BETTER_KICKER,
]

FLUSH_DOMINATING_WEAKER_HANDS = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "5_OF_SPADES",
        "7_OF_SPADES",
        "8_OF_SPADES",
        "9_OF_HEARTS",
    ]
)

POCKET_4S = make_hole_cards_for_testing(
    [
        "4_OF_CLUBS",
        "4_OF_DIAMONDS",
    ]
)

HOLE_CARDS_4_5_HEARTS = make_hole_cards_for_testing(
    [
        "4_OF_HEARTS",
        "5_OF_HEARTS",
    ]
)


def test_flush():
    hand_type_test_builder(
        hand_tested="flush",
        valid_cases_in_ascending_strength=VALID_FLUSH_CASES_IN_ASCENDING_ORDER,
        expected_hand_type_score=FLUSH_HAND_TYPE_SCORE,
        valid_tie_case_1=COMMUNITY_FLUSH_9_HI_SPADES,
        valid_tie_case_2=FLUSH_9_HI_DIAMONDS,
    )


def test_compare_flushes():
    logger.debug("Test that the stronger flush is always the winner")
    assert_winner_regardless_of_order(
        community_cards=COMMUNITY_FLUSH_9_HI_SPADES,
        winning_hole_cards=HOLE_CARDS_KING_QUEEN_SPADES,
        losing_hole_cards=HOLE_CARDS_2_3_SPADES,
    )


def test_community_flush_ties():
    logger.debug("Test that a community flush is always a tie")
    assert_tie_regardless_of_order(
        community_cards=COMMUNITY_FLUSH_9_HI_SPADES,
        hole_cards_1=POCKET_9S,
        hole_cards_2=POCKET_ACES,
    )


# TODO: Implement all below since not yet implemented since building for full houses
def test_compare_flush_to_other_hands():
    logger.debug("Test that a flush beats a straight")
    assert_winner_regardless_of_order(
        community_cards=FLUSH_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=HOLE_CARDS_2_3_SPADES,
        losing_hole_cards=HOLE_CARDS_3_6_HEARTS,
    )

    logger.debug("Test that a flush beats a three of a kind")
    assert_winner_regardless_of_order(
        community_cards=FLUSH_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=HOLE_CARDS_2_3_SPADES,
        losing_hole_cards=POCKET_4S,
    )

    logger.debug("Test that a flush beats a two pair")
    assert_winner_regardless_of_order(
        community_cards=FLUSH_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=HOLE_CARDS_2_3_SPADES,
        losing_hole_cards=HOLE_CARDS_4_5_HEARTS,
    )

    logger.debug("Test that a flush beats a pair")
    assert_winner_regardless_of_order(
        community_cards=FLUSH_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=HOLE_CARDS_2_3_SPADES,
        losing_hole_cards=HOLE_CARDS_KING_9_CLUBS,
    )


# TODO: Continue with tests for straight, then three of a kind, then two pair, then pair

# TODO: Extend this for determining the winner between multiple players, probably by extending the Hand class?

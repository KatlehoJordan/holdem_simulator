from src.config import logger
from src.player_hand import (
    assert_tie_regardless_of_order,
    assert_winner_regardless_of_order,
)
from tests.test_straight_flush import COMMUNITY_ROYAL_FLUSH
from tests.tests_config import (
    HOLE_CARDS_2_3_SPADES,
    make_community_cards_for_testing,
    make_hole_cards_for_testing,
)

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


# TODO: Continue with tests for full house, then flush, then straight, then three of a kind, then two pair, then pair

# TODO: Extend this for determining the winner between multiple players, probably by extending the Hand class?

from src.flush import FLUSH_HAND_TYPE_SCORE
from tests.tests_config import hand_type_test_builder, make_community_cards_for_testing

FLUSH_9_HI_SPADES = make_community_cards_for_testing(
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
    FLUSH_9_HI_SPADES,
    FLUSH_9_HI_DIAMONDS,
    FLUSH_10_HI_SPADES,
    FLUSH_10_HI_SPADES_BETTER_KICKER,
]


def test_flush():
    hand_type_test_builder(
        hand_tested="flush",
        valid_cases_in_ascending_strength=VALID_FLUSH_CASES_IN_ASCENDING_ORDER,
        expected_hand_type_score=FLUSH_HAND_TYPE_SCORE,
        valid_tie_case_1=FLUSH_9_HI_SPADES,
        valid_tie_case_2=FLUSH_9_HI_DIAMONDS,
    )


# TODO: Implement all below since not yet implemented since building for full houses
def test_compare_flushes():
    logger.debug("Test that the stronger flush is always the winner")
    assert_winner_regardless_of_order(
        community_cards=COMMUNITY_FULL_HOUSE_ACES_OVER_KINGS,
        winning_hole_cards=HOLE_CARDS_ACE_KING_HEARTS,
        losing_hole_cards=HOLE_CARDS_KING_QUEEN_SPADES,
    )


def test_community_flush_ties():
    logger.debug("Test that a community flush is always a tie")
    assert_tie_regardless_of_order(
        community_cards=COMMUNITY_FULL_HOUSE_ACES_OVER_KINGS,
        hole_cards_1=HOLE_CARDS_KING_QUEEN_SPADES,
        hole_cards_2=HOLE_CARDS_2_3_HEARTS,
    )


def test_compare_flush_to_other_hands():
    logger.debug("Test that a flush beats a straight")
    assert_winner_regardless_of_order(
        community_cards=FULL_HOUSE_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=HOLE_CARDS_2_3_HEARTS,
        losing_hole_cards=HOLE_CARDS_ACE_KING_HEARTS,
    )

    logger.debug("Test that a flush beats a three of a kind")
    assert_winner_regardless_of_order(
        community_cards=FULL_HOUSE_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=HOLE_CARDS_2_3_HEARTS,
        losing_hole_cards=HOLE_CARDS_3_6_HEARTS,
    )

    logger.debug("Test that a flush beats a two pair")
    assert_winner_regardless_of_order(
        community_cards=FULL_HOUSE_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=HOLE_CARDS_2_3_HEARTS,
        losing_hole_cards=POCKET_9S,
    )

    logger.debug("Test that a flush beats a pair")
    assert_winner_regardless_of_order(
        community_cards=FULL_HOUSE_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=HOLE_CARDS_2_3_HEARTS,
        losing_hole_cards=HOLE_CARDS_KING_9_CLUBS,
    )


# TODO: Continue with tests for flush, then flush, then straight, then three of a kind, then two pair, then pair

# TODO: Extend this for determining the winner between multiple players, probably by extending the Hand class?

from src.config import logger
from src.player_hand import (
    assert_tie_regardless_of_order,
    assert_winner_regardless_of_order,
)
from src.two_pair import TWO_PAIR_HAND_TYPE_SCORE
from tests.test_straight import HOLE_CARDS_10_JACK_SPADES
from tests.test_straight_flush import HOLE_CARDS_2_7_SPADES_DIAMONDS
from tests.tests_config import hand_type_test_builder, make_community_cards_for_testing

TWO_PAIR_3S_AND_2S_WEAKER_KICKER = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "3_OF_HEARTS",
        "4_OF_SPADES",
        "7_OF_DIAMONDS",
        "KING_OF_SPADES",
    ]
)

TWO_PAIR_3S_AND_2S = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "3_OF_HEARTS",
        "4_OF_SPADES",
        "7_OF_DIAMONDS",
        "ACE_OF_SPADES",
    ]
)

TWO_PAIR_3S_AND_2S_ALTERNATE = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "3_OF_HEARTS",
        "4_OF_SPADES",
        "7_OF_DIAMONDS",
        "ACE_OF_HEARTS",
    ]
)

TWO_PAIR_4S_AND_5S_WEAKER_KICKER = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "4_OF_SPADES",
        "5_OF_HEARTS",
        "5_OF_CLUBS",
        "KING_OF_SPADES",
    ]
)

TWO_PAIR_4S_AND_5S = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "4_OF_HEARTS",
        "5_OF_CLUBS",
        "5_OF_DIAMONDS",
        "ACE_OF_SPADES",
    ]
)

COMMUNITY_TWO_PAIR_ACES_AND_KINGS = make_community_cards_for_testing(
    [
        "ACE_OF_DIAMONDS",
        "ACE_OF_HEARTS",
        "KING_OF_CLUBS",
        "KING_OF_HEARTS",
        "9_OF_SPADES",
    ]
)

VALID_TWO_PAIR_CASES_IN_ASCENDING_STRENGTH = [
    TWO_PAIR_3S_AND_2S_WEAKER_KICKER,
    TWO_PAIR_3S_AND_2S,
    TWO_PAIR_3S_AND_2S_ALTERNATE,
    TWO_PAIR_4S_AND_5S_WEAKER_KICKER,
    TWO_PAIR_4S_AND_5S,
    COMMUNITY_TWO_PAIR_ACES_AND_KINGS,
]


def test_two_pair():
    hand_type_test_builder(
        hand_tested="two pair",
        valid_cases_in_ascending_strength=VALID_TWO_PAIR_CASES_IN_ASCENDING_STRENGTH,
        expected_hand_type_score=TWO_PAIR_HAND_TYPE_SCORE,
        valid_tie_case_1=TWO_PAIR_3S_AND_2S,
        valid_tie_case_2=TWO_PAIR_3S_AND_2S_ALTERNATE,
    )


def test_compare_two_pairs():
    logger.debug("Test that the stronger two pair is always the winner")
    assert_winner_regardless_of_order(
        community_cards=COMMUNITY_TWO_PAIR_ACES_AND_KINGS,
        winning_hole_cards=HOLE_CARDS_10_JACK_SPADES,
        losing_hole_cards=HOLE_CARDS_2_7_SPADES_DIAMONDS,
    )


# TODO: Implement all below since not yet implemented
def test_community_two_pair_ties():
    logger.debug("Test that a community two pair is always a tie")
    assert_tie_regardless_of_order(
        community_cards=COMMUNITY_THREE_OF_A_KIND_ACES,
        hole_cards_1=HOLE_CARDS_2_3_HEARTS,
        hole_cards_2=HOLE_CARDS_2_3_SPADES,
    )


def test_compare_two_pair_to_other_hands():
    logger.debug("Test that a two pair beats a two pair")
    assert_winner_regardless_of_order(
        community_cards=THREE_OF_A_KIND_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=POCKET_6S,
        losing_hole_cards=HOLE_CARDS_4_5_HEARTS,
    )

    logger.debug("Test that a two pair beats a pair")
    assert_winner_regardless_of_order(
        community_cards=THREE_OF_A_KIND_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=POCKET_6S,
        losing_hole_cards=HOLE_CARDS_KING_9_CLUBS,
    )

    logger.debug("Test that a two pair beats a high card")
    assert_winner_regardless_of_order(
        community_cards=THREE_OF_A_KIND_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=POCKET_6S,
        losing_hole_cards=HOLE_CARDS_KING_QUEEN_SPADES,
    )


# TODO: Continue with tests for two pair, then two pair, then two pair, then pair

# TODO: Extend this for determining the winner between multiple players, probably by extending the Hand class?

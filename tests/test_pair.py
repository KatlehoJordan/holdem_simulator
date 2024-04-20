from src.config import logger
from src.pair import PAIR_HAND_TYPE_SCORE
from src.player_hand import (
    assert_tie_regardless_of_order,
    assert_winner_regardless_of_order,
)
from tests.test_straight_flush import (
    HOLE_CARDS_2_7_SPADES_DIAMONDS,
    HOLE_CARDS_ACE_KING_HEARTS,
    HOLE_CARDS_KING_9_CLUBS,
)
from tests.tests_config import (
    HOLE_CARDS_2_3_SPADES,
    hand_type_test_builder,
    make_community_cards_for_testing,
)

PAIR_OF_2S = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "4_OF_SPADES",
        "QUEEN_OF_HEARTS",
        "KING_OF_DIAMONDS",
        "ACE_OF_SPADES",
    ]
)

PAIR_OF_2S_ALTERNATE = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "4_OF_SPADES",
        "QUEEN_OF_HEARTS",
        "KING_OF_DIAMONDS",
        "ACE_OF_HEARTS",
    ]
)

PAIR_OF_2S_MODERATE_KICKERS = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "4_OF_SPADES",
        "JACK_OF_HEARTS",
        "KING_OF_DIAMONDS",
        "ACE_OF_SPADES",
    ]
)

PAIR_OF_2S_WEAK_KICKERS = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "4_OF_SPADES",
        "JACK_OF_HEARTS",
        "QUEEN_OF_DIAMONDS",
        "ACE_OF_SPADES",
    ]
)

PAIR_OF_2S_WEAKEST_KICKERS = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "4_OF_SPADES",
        "JACK_OF_HEARTS",
        "QUEEN_OF_DIAMONDS",
        "KING_OF_SPADES",
    ]
)

PAIR_OF_3S = make_community_cards_for_testing(
    [
        "3_OF_DIAMONDS",
        "4_OF_SPADES",
        "QUEEN_OF_HEARTS",
        "KING_OF_DIAMONDS",
        "ACE_OF_SPADES",
    ]
)

PAIR_OF_4S = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "4_OF_SPADES",
        "QUEEN_OF_HEARTS",
        "KING_OF_DIAMONDS",
        "ACE_OF_SPADES",
    ]
)

COMMUNITY_PAIR_OF_ACES = make_community_cards_for_testing(
    [
        "8_OF_SPADES",
        "10_OF_DIAMONDS",
        "QUEEN_OF_HEARTS",
        "ACE_OF_DIAMONDS",
        "ACE_OF_SPADES",
    ]
)

VALID_PAIR_CASES_IN_ASCENDING_STRENGTH = [
    PAIR_OF_2S_WEAKEST_KICKERS,
    PAIR_OF_2S_WEAK_KICKERS,
    PAIR_OF_2S_MODERATE_KICKERS,
    PAIR_OF_2S,
    PAIR_OF_2S_ALTERNATE,
    PAIR_OF_3S,
    PAIR_OF_4S,
    COMMUNITY_PAIR_OF_ACES,
]

PAIR_DOMINATING_WEAKER_HANDS = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "5_OF_CLUBS",
        "6_OF_HEARTS",
        "9_OF_HEARTS",
        "ACE_OF_SPADES",
    ]
)

# TODO: Delete this after veryfing pre-commit hooks are working


def test_pair():
    hand_type_test_builder(
        hand_tested="pair",
        valid_cases_in_ascending_strength=VALID_PAIR_CASES_IN_ASCENDING_STRENGTH,
        expected_hand_type_score=PAIR_HAND_TYPE_SCORE,
        valid_tie_case_1=PAIR_OF_2S,
        valid_tie_case_2=PAIR_OF_2S_ALTERNATE,
    )


def test_compare_pairs():
    logger.debug("Test that the stronger pair is always the winner")
    assert_winner_regardless_of_order(
        community_cards=COMMUNITY_PAIR_OF_ACES,
        winning_hole_cards=HOLE_CARDS_KING_9_CLUBS,
        losing_hole_cards=HOLE_CARDS_2_7_SPADES_DIAMONDS,
    )


def test_community_pair_ties():
    logger.debug("Test that a community pair is always a tie")
    assert_tie_regardless_of_order(
        community_cards=COMMUNITY_PAIR_OF_ACES,
        hole_cards_1=HOLE_CARDS_2_7_SPADES_DIAMONDS,
        hole_cards_2=HOLE_CARDS_2_3_SPADES,
    )


def test_compare_pair_to_other_hands():
    logger.debug("Test that a pair beats a high card")
    assert_winner_regardless_of_order(
        community_cards=PAIR_DOMINATING_WEAKER_HANDS,
        winning_hole_cards=HOLE_CARDS_ACE_KING_HEARTS,
        losing_hole_cards=HOLE_CARDS_2_7_SPADES_DIAMONDS,
    )

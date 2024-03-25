from src.config import logger
from src.full_house import FULL_HOUSE_HAND_TYPE_SCORE
from src.player_hand import (
    assert_tie_regardless_of_order,
    assert_winner_regardless_of_order,
)
from tests.test_straight_flush import (
    HOLE_CARDS_2_3_HEARTS,
    HOLE_CARDS_ACE_KING_HEARTS,
    HOLE_CARDS_KING_QUEEN_SPADES,
)
from tests.tests_config import hand_type_test_builder, make_community_cards_for_testing

FULL_HOUSE_2S_OVER_3S = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "2_OF_HEARTS",
        "3_OF_CLUBS",
        "4_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

FULL_HOUSE_2S_OVER_3S_ALTERNATE = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "2_OF_HEARTS",
        "3_OF_DIAMONDS",
        "5_OF_SPADES",
        "ACE_OF_DIAMONDS",
    ]
)

FULL_HOUSE_3S_OVER_2S = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "3_OF_HEARTS",
        "3_OF_CLUBS",
        "4_OF_SPADES",
        "5_OF_DIAMONDS",
    ]
)

FOUR_OF_A_KIND_4S_OVER_5S = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "4_OF_HEARTS",
        "4_OF_CLUBS",
        "5_OF_SPADES",
        "5_OF_DIAMONDS",
    ]
)

FOUR_OF_A_KIND_ACES_OVER_KINGS = make_community_cards_for_testing(
    [
        "ACE_OF_DIAMONDS",
        "ACE_OF_HEARTS",
        "ACE_OF_CLUBS",
        "KING_OF_SPADES",
        "KING_OF_DIAMONDS",
    ]
)

VALID_FOUR_OF_A_KIND_CASES_IN_ASCENDING_STRENGTH = [
    FULL_HOUSE_2S_OVER_3S,
    FULL_HOUSE_2S_OVER_3S_ALTERNATE,
    FULL_HOUSE_3S_OVER_2S,
    FOUR_OF_A_KIND_4S_OVER_5S,
    FOUR_OF_A_KIND_ACES_OVER_KINGS,
]

FULL_HOUSE_ACES_OR_KINGS = make_community_cards_for_testing(
    [
        "ACE_OF_SPADES",
        "ACE_OF_DIAMONDS",
        "9_OF_CLUBS",
        "KING_OF_CLUBS",
        "KING_OF_DIAMONDS",
    ]
)

COMMUNITY_FULL_HOUSE = make_community_cards_for_testing(
    [
        "ACE_OF_SPADES",
        "ACE_OF_DIAMONDS",
        "ACE_OF_CLUBS",
        "KING_OF_CLUBS",
        "KING_OF_DIAMONDS",
    ]
)


def test_full_house():
    hand_type_test_builder(
        hand_tested="full house",
        valid_cases_in_ascending_strength=VALID_FOUR_OF_A_KIND_CASES_IN_ASCENDING_STRENGTH,
        expected_hand_type_score=FULL_HOUSE_HAND_TYPE_SCORE,
        valid_tie_case_1=FULL_HOUSE_2S_OVER_3S,
        valid_tie_case_2=FULL_HOUSE_2S_OVER_3S_ALTERNATE,
    )


def test_compare_full_houses():
    logger.debug("Test that the stronger full house is always the winner")
    assert_winner_regardless_of_order(
        community_cards=FULL_HOUSE_ACES_OR_KINGS,
        winning_hole_cards=HOLE_CARDS_ACE_KING_HEARTS,
        losing_hole_cards=HOLE_CARDS_KING_QUEEN_SPADES,
    )


def test_community_full_house_ties():
    logger.debug("Test that a community full house is always a tie")
    assert_tie_regardless_of_order(
        community_cards=COMMUNITY_FULL_HOUSE,
        hole_cards_1=HOLE_CARDS_KING_QUEEN_SPADES,
        hole_cards_2=HOLE_CARDS_2_3_HEARTS,
    )


# TODO: Finish building this since not yet adapted to full houses
# def test_compare_full_house_to_other_hands():
#     logger.debug("Test that a full house beats a flush")
#     assert_winner_regardless_of_order(
#         community_cards=FOUR_OF_A_KIND_DOMINATING_WEAKER_HANDS,
#         winning_hole_cards=POCKET_6S,
#         losing_hole_cards=HOLE_CARDS_KING_QUEEN_SPADES,
#     )

#     logger.debug("Test that a full house beats a straight")
#     assert_winner_regardless_of_order(
#         community_cards=FOUR_OF_A_KIND_DOMINATING_WEAKER_HANDS,
#         winning_hole_cards=POCKET_6S,
#         losing_hole_cards=HOLE_CARDS_2_3_HEARTS,
#     )

#     logger.debug("Test that a full house beats a three of a kind")
#     assert_winner_regardless_of_order(
#         community_cards=FOUR_OF_A_KIND_DOMINATING_THREE_OF_A_KIND,
#         winning_hole_cards=HOLE_CARDS_6_7_DIAMONDS,
#         losing_hole_cards=HOLE_CARDS_KING_9_CLUBS,
#     )

#     logger.debug("Test that a full house beats a two pair")
#     assert_winner_regardless_of_order(
#         community_cards=FOUR_OF_A_KIND_DOMINATING_WEAKER_HANDS,
#         winning_hole_cards=POCKET_6S,
#         losing_hole_cards=HOLE_CARDS_KING_9_CLUBS,
#     )

#     logger.debug("Test that a full house beats a pair")
#     assert_winner_regardless_of_order(
#         community_cards=FOUR_OF_A_KIND_DOMINATING_WEAKER_HANDS,
#         winning_hole_cards=POCKET_6S,
#         losing_hole_cards=HOLE_CARDS_ACE_KING_HEARTS,
#     )


# TODO: Continue with tests for full house, then flush, then straight, then three of a kind, then two pair, then pair

# TODO: Extend this for determining the winner between multiple players, probably by extending the Hand class?

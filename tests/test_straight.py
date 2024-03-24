from src.straight import STRAIGHT_HAND_TYPE_SCORE
from tests.tests_config import hand_type_test_builder, make_community_cards_for_testing

STRAIGHT_5_HI = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "5_OF_DIAMONDS",
        "9_OF_DIAMONDS",
        "10_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

STRAIGHT_5_HI_ALTERNATE = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "5_OF_DIAMONDS",
        "9_OF_DIAMONDS",
        "10_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

STRAIGHT_6_HI = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "5_OF_DIAMONDS",
        "6_OF_DIAMONDS",
        "10_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

VALID_STRAIGHT_CASES_IN_ASCENDING_ORDER = [
    STRAIGHT_5_HI,
    STRAIGHT_5_HI_ALTERNATE,
    STRAIGHT_6_HI,
]


def test_straight():
    hand_type_test_builder(
        hand_tested="straight",
        valid_cases_in_ascending_strength=VALID_STRAIGHT_CASES_IN_ASCENDING_ORDER,
        expected_hand_type_score=STRAIGHT_HAND_TYPE_SCORE,
        valid_tie_case_1=STRAIGHT_5_HI,
        valid_tie_case_2=STRAIGHT_5_HI_ALTERNATE,
    )

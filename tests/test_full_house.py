from src.full_house import FULL_HOUSE_HAND_TYPE_SCORE
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


def test_full_house():
    hand_type_test_builder(
        hand_tested="full house",
        valid_cases_in_ascending_strength=VALID_FOUR_OF_A_KIND_CASES_IN_ASCENDING_STRENGTH,
        expected_hand_type_score=FULL_HOUSE_HAND_TYPE_SCORE,
        valid_tie_case_1=FULL_HOUSE_2S_OVER_3S,
        valid_tie_case_2=FULL_HOUSE_2S_OVER_3S_ALTERNATE,
    )

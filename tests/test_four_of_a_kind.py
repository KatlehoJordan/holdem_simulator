from src.four_of_a_kind import FOUR_OF_A_KIND_HAND_TYPE_SCORE
from tests.tests_config import hand_type_test_builder, make_community_cards_for_testing

# TODO: Simplify this to a function since so much is repeated

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


def test_four_of_a_kind():
    hand_type_test_builder(
        hand_tested="four of a kind",
        valid_cases_in_ascending_strength=VALID_FOUR_OF_A_KIND_CASES_IN_ASCENDING_STRENGTH,
        expected_hand_type_score=FOUR_OF_A_KIND_HAND_TYPE_SCORE,
        valid_tie_case_1=FOUR_OF_A_KIND_2S,
        valid_tie_case_2=FOUR_OF_A_KIND_2S_ALTERNATE,
    )

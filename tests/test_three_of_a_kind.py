from src.three_of_a_kind import THREE_OF_A_KIND_HAND_TYPE_SCORE
from tests.tests_config import hand_type_test_builder, make_community_cards_for_testing

THREE_OF_A_KIND_2S = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "2_OF_HEARTS",
        "4_OF_SPADES",
        "7_OF_DIAMONDS",
        "ACE_OF_SPADES",
    ]
)

THREE_OF_A_KIND_2S_ALTERNATE = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "2_OF_CLUBS",
        "4_OF_SPADES",
        "7_OF_DIAMONDS",
        "ACE_OF_DIAMONDS",
    ]
)

THREE_OF_A_KIND_2S_WEAKER_KICKERS = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "2_OF_HEARTS",
        "4_OF_SPADES",
        "7_OF_DIAMONDS",
        "KING_OF_SPADES",
    ]
)

THREE_OF_A_KIND_2S_WEAKEST_KICKERS = make_community_cards_for_testing(
    [
        "2_OF_DIAMONDS",
        "2_OF_HEARTS",
        "4_OF_SPADES",
        "6_OF_DIAMONDS",
        "KING_OF_SPADES",
    ]
)

THREE_OF_A_KIND_3S = make_community_cards_for_testing(
    [
        "3_OF_DIAMONDS",
        "3_OF_HEARTS",
        "4_OF_SPADES",
        "7_OF_DIAMONDS",
        "ACE_OF_SPADES",
    ]
)

THREE_OF_A_KIND_4S = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "4_OF_HEARTS",
        "4_OF_CLUBS",
        "7_OF_DIAMONDS",
        "ACE_OF_SPADES",
    ]
)

THREE_OF_A_KIND_ACES = make_community_cards_for_testing(
    [
        "ACE_OF_DIAMONDS",
        "ACE_OF_HEARTS",
        "ACE_OF_CLUBS",
        "7_OF_DIAMONDS",
        "4_OF_SPADES",
    ]
)

VALID_THREE_OF_A_KIND_CASES_IN_ASCENDING_STRENGTH = [
    THREE_OF_A_KIND_2S_WEAKEST_KICKERS,
    THREE_OF_A_KIND_2S_WEAKER_KICKERS,
    THREE_OF_A_KIND_2S,
    THREE_OF_A_KIND_2S_ALTERNATE,
    THREE_OF_A_KIND_3S,
    THREE_OF_A_KIND_4S,
    THREE_OF_A_KIND_ACES,
]


def test_three_of_a_kind():
    hand_type_test_builder(
        hand_tested="three of a kind",
        valid_cases_in_ascending_strength=VALID_THREE_OF_A_KIND_CASES_IN_ASCENDING_STRENGTH,
        expected_hand_type_score=THREE_OF_A_KIND_HAND_TYPE_SCORE,
        valid_tie_case_1=THREE_OF_A_KIND_2S,
        valid_tie_case_2=THREE_OF_A_KIND_2S_ALTERNATE,
    )

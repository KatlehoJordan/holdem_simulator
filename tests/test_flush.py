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

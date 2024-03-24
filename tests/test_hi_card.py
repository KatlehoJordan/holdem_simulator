from src.hi_card import HI_CARD_HAND_TYPE_SCORE
from tests.tests_config import hand_type_test_builder, make_community_cards_for_testing

HI_CARD_9 = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "5_OF_DIAMONDS",
        "7_OF_DIAMONDS",
        "8_OF_SPADES",
        "9_OF_SPADES",
    ]
)

HI_CARD_10_9 = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "5_OF_DIAMONDS",
        "7_OF_DIAMONDS",
        "9_OF_SPADES",
        "10_OF_SPADES",
    ]
)

HI_CARD_10_8 = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "5_OF_DIAMONDS",
        "7_OF_DIAMONDS",
        "8_OF_SPADES",
        "10_OF_SPADES",
    ]
)

HI_CARD_10_8_ALTERNATE = make_community_cards_for_testing(
    [
        "4_OF_DIAMONDS",
        "5_OF_DIAMONDS",
        "7_OF_DIAMONDS",
        "8_OF_DIAMONDS",
        "10_OF_SPADES",
    ]
)

VALID_HI_CARD_CASES_IN_ASCENDING_ORDER = [
    HI_CARD_9,
    HI_CARD_10_8,
    HI_CARD_10_8_ALTERNATE,
    HI_CARD_10_9,
]


def test_hi_card():
    hand_type_test_builder(
        hand_tested="hi card",
        valid_cases_in_ascending_strength=VALID_HI_CARD_CASES_IN_ASCENDING_ORDER,
        expected_hand_type_score=HI_CARD_HAND_TYPE_SCORE,
        valid_tie_case_1=HI_CARD_10_8,
        valid_tie_case_2=HI_CARD_10_8_ALTERNATE,
    )

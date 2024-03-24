from src.straight_flush import STRAIGHT_FLUSH_HAND_TYPE_SCORE
from tests.tests_config import hand_type_test_builder, make_community_cards_for_testing

STRAIGHT_FLUSH_5_HI_SPADES = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "5_OF_SPADES",
        "9_OF_SPADES",
        "10_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

STRAIGHT_FLUSH_5_HI_SPADES_ALTERNATE = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "5_OF_SPADES",
        "8_OF_SPADES",
        "9_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

STRAIGHT_FLUSH_7_HI_SPADES = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "5_OF_SPADES",
        "6_OF_SPADES",
        "7_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

STRAIGHT_FLUSH_9_HI_SPADES = make_community_cards_for_testing(
    [
        "5_OF_SPADES",
        "6_OF_SPADES",
        "7_OF_SPADES",
        "8_OF_SPADES",
        "9_OF_SPADES",
    ]
)

STRAIGHT_FLUSH_ACE_HI_SPADES = make_community_cards_for_testing(
    [
        "10_OF_SPADES",
        "JACK_OF_SPADES",
        "QUEEN_OF_SPADES",
        "KING_OF_SPADES",
        "ACE_OF_SPADES",
    ]
)

VALID_STRAIGHT_FLUSH_CASES_IN_ASCENDING_STRENGTH = [
    STRAIGHT_FLUSH_5_HI_SPADES,
    STRAIGHT_FLUSH_5_HI_SPADES_ALTERNATE,
    STRAIGHT_FLUSH_7_HI_SPADES,
    STRAIGHT_FLUSH_9_HI_SPADES,
    STRAIGHT_FLUSH_ACE_HI_SPADES,
]


def test_straight_flush():
    hand_type_test_builder(
        hand_tested="straight flush",
        valid_cases_in_ascending_strength=VALID_STRAIGHT_FLUSH_CASES_IN_ASCENDING_STRENGTH,
        expected_hand_type_score=STRAIGHT_FLUSH_HAND_TYPE_SCORE,
        valid_tie_case_1=STRAIGHT_FLUSH_5_HI_SPADES,
        valid_tie_case_2=STRAIGHT_FLUSH_5_HI_SPADES_ALTERNATE,
    )

from src.two_pair import TWO_PAIR_HAND_TYPE_SCORE
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

TWO_PAIR_ACES_AND_KINGS = make_community_cards_for_testing(
    [
        "ACE_OF_DIAMONDS",
        "ACE_OF_HEARTS",
        "KING_OF_CLUBS",
        "KING_OF_HEARTS",
        "4_OF_SPADES",
    ]
)

VALID_TWO_PAIR_CASES_IN_ASCENDING_STRENGTH = [
    TWO_PAIR_3S_AND_2S_WEAKER_KICKER,
    TWO_PAIR_3S_AND_2S,
    TWO_PAIR_3S_AND_2S_ALTERNATE,
    TWO_PAIR_4S_AND_5S_WEAKER_KICKER,
    TWO_PAIR_4S_AND_5S,
    TWO_PAIR_ACES_AND_KINGS,
]


def test_two_pair():
    hand_type_test_builder(
        hand_tested="two pair",
        valid_cases_in_ascending_strength=VALID_TWO_PAIR_CASES_IN_ASCENDING_STRENGTH,
        expected_hand_type_score=TWO_PAIR_HAND_TYPE_SCORE,
        valid_tie_case_1=TWO_PAIR_3S_AND_2S,
        valid_tie_case_2=TWO_PAIR_3S_AND_2S_ALTERNATE,
    )

from src.pair import PAIR_HAND_TYPE_SCORE
from tests.tests_config import hand_type_test_builder, make_community_cards_for_testing

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

PAIR_OF_ACES = make_community_cards_for_testing(
    [
        "4_OF_SPADES",
        "6_OF_DIAMONDS",
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
    PAIR_OF_ACES,
]


def test_pair():
    hand_type_test_builder(
        hand_tested="pair",
        valid_cases_in_ascending_strength=VALID_PAIR_CASES_IN_ASCENDING_STRENGTH,
        expected_hand_type_score=PAIR_HAND_TYPE_SCORE,
        valid_tie_case_1=PAIR_OF_2S,
        valid_tie_case_2=PAIR_OF_2S_ALTERNATE,
    )

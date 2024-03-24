from src.community_cards import CommunityCards
from src.deck import Deck
from src.three_of_a_kind import THREE_OF_A_KIND_HAND_TYPE_SCORE
from tests.tests_config import CARDS_DICT, hand_type_test_builder

THREE_OF_A_KIND_2S = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["2_OF_DIAMONDS"],
    card2=CARDS_DICT["2_OF_HEARTS"],
    card3=CARDS_DICT["4_OF_SPADES"],
    card4=CARDS_DICT["7_OF_DIAMONDS"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

THREE_OF_A_KIND_2S_ALTERNATE = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["2_OF_DIAMONDS"],
    card2=CARDS_DICT["2_OF_CLUBS"],
    card3=CARDS_DICT["4_OF_SPADES"],
    card4=CARDS_DICT["7_OF_DIAMONDS"],
    card5=CARDS_DICT["ACE_OF_DIAMONDS"],
)

THREE_OF_A_KIND_2S_WEAKER_KICKERS = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["2_OF_DIAMONDS"],
    card2=CARDS_DICT["2_OF_HEARTS"],
    card3=CARDS_DICT["4_OF_SPADES"],
    card4=CARDS_DICT["7_OF_DIAMONDS"],
    card5=CARDS_DICT["KING_OF_SPADES"],
)

THREE_OF_A_KIND_2S_WEAKEST_KICKERS = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["2_OF_DIAMONDS"],
    card2=CARDS_DICT["2_OF_HEARTS"],
    card3=CARDS_DICT["4_OF_SPADES"],
    card4=CARDS_DICT["6_OF_DIAMONDS"],
    card5=CARDS_DICT["KING_OF_SPADES"],
)

THREE_OF_A_KIND_3S = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["3_OF_DIAMONDS"],
    card2=CARDS_DICT["3_OF_HEARTS"],
    card3=CARDS_DICT["4_OF_SPADES"],
    card4=CARDS_DICT["7_OF_DIAMONDS"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

THREE_OF_A_KIND_4S = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["4_OF_HEARTS"],
    card3=CARDS_DICT["4_OF_CLUBS"],
    card4=CARDS_DICT["7_OF_DIAMONDS"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

THREE_OF_A_KIND_ACES = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["ACE_OF_DIAMONDS"],
    card2=CARDS_DICT["ACE_OF_HEARTS"],
    card3=CARDS_DICT["ACE_OF_CLUBS"],
    card4=CARDS_DICT["7_OF_DIAMONDS"],
    card5=CARDS_DICT["4_OF_SPADES"],
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

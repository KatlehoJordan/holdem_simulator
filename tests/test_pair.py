from src.community_cards import CommunityCards
from src.deck import Deck
from src.pair import PAIR_HAND_TYPE_SCORE
from tests.tests_config import CARDS_DICT, hand_type_test_builder

PAIR_OF_2S = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["2_OF_DIAMONDS"],
    card2=CARDS_DICT["4_OF_SPADES"],
    card3=CARDS_DICT["QUEEN_OF_HEARTS"],
    card4=CARDS_DICT["KING_OF_DIAMONDS"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

PAIR_OF_2S_ALTERNATE = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["2_OF_DIAMONDS"],
    card2=CARDS_DICT["4_OF_SPADES"],
    card3=CARDS_DICT["QUEEN_OF_HEARTS"],
    card4=CARDS_DICT["KING_OF_DIAMONDS"],
    card5=CARDS_DICT["ACE_OF_HEARTS"],
)

PAIR_OF_2S_MODERATE_KICKERS = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["2_OF_DIAMONDS"],
    card2=CARDS_DICT["4_OF_SPADES"],
    card3=CARDS_DICT["JACK_OF_HEARTS"],
    card4=CARDS_DICT["KING_OF_DIAMONDS"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

PAIR_OF_2S_WEAK_KICKERS = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["2_OF_DIAMONDS"],
    card2=CARDS_DICT["4_OF_SPADES"],
    card3=CARDS_DICT["JACK_OF_HEARTS"],
    card4=CARDS_DICT["QUEEN_OF_DIAMONDS"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

PAIR_OF_2S_WEAKEST_KICKERS = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["2_OF_DIAMONDS"],
    card2=CARDS_DICT["4_OF_SPADES"],
    card3=CARDS_DICT["JACK_OF_HEARTS"],
    card4=CARDS_DICT["QUEEN_OF_DIAMONDS"],
    card5=CARDS_DICT["KING_OF_SPADES"],
)

PAIR_OF_3S = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["3_OF_DIAMONDS"],
    card2=CARDS_DICT["4_OF_SPADES"],
    card3=CARDS_DICT["QUEEN_OF_HEARTS"],
    card4=CARDS_DICT["KING_OF_DIAMONDS"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

PAIR_OF_4S = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["4_OF_SPADES"],
    card3=CARDS_DICT["QUEEN_OF_HEARTS"],
    card4=CARDS_DICT["KING_OF_DIAMONDS"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

PAIR_OF_ACES = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_SPADES"],
    card2=CARDS_DICT["6_OF_DIAMONDS"],
    card3=CARDS_DICT["QUEEN_OF_HEARTS"],
    card4=CARDS_DICT["ACE_OF_DIAMONDS"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
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

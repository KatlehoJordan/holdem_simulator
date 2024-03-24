from src.card import Card
from src.community_cards import CommunityCards
from src.config import VALID_RANKS_DICT, VALID_SUITS, logger
from src.deck import Deck
from src.hole_cards import HoleCards
from src.player_hand import PlayerHand
from src.rank import Rank
from src.suit import Suit

CARDS_DICT = {}

for suit in VALID_SUITS:
    for rank in VALID_RANKS_DICT.keys():
        card_name = f"{rank.upper()}_OF_{suit.upper()}"
        CARDS_DICT[card_name] = Card(Suit(suit), Rank(rank))

HOLE_CARDS_2_3_SPADES = HoleCards(
    deck=Deck(), card1=CARDS_DICT["2_OF_SPADES"], card2=CARDS_DICT["3_OF_SPADES"]
)


def hand_type_test_builder(
    hand_tested: str,
    valid_cases_in_ascending_strength: list,
    expected_hand_type_score: int,
    valid_tie_case_1: CommunityCards,
    valid_tie_case_2: CommunityCards,
    hole_cards: HoleCards = HOLE_CARDS_2_3_SPADES,
):
    logger.debug(
        "Test that every %s tested has the correct hand type score", hand_tested
    )
    for community_cards in valid_cases_in_ascending_strength:
        assert (
            PlayerHand(
                hole_cards=hole_cards,
                community_cards=community_cards,
            ).hand_type.hand_type_score
            == expected_hand_type_score
        )

    logger.debug(
        "Test that every %s is ranked in correct order based on top rank", hand_tested
    )
    hand_types = [
        PlayerHand(hole_cards=hole_cards, community_cards=community_cards).hand_type
        for community_cards in valid_cases_in_ascending_strength
    ]
    top_ranks = [hand_type.top_ranks[0] for hand_type in hand_types]
    assert top_ranks == sorted(top_ranks)

    logger.debug("Test that %s ties are detected", hand_tested)
    assert (
        PlayerHand(
            hole_cards=hole_cards, community_cards=valid_tie_case_1
        ).hand_type.top_ranks
        == PlayerHand(
            hole_cards=hole_cards, community_cards=valid_tie_case_2
        ).hand_type.top_ranks
    )

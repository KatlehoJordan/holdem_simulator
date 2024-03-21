from src.community_cards import CommunityCards
from src.deck import Deck
from src.hi_card import HI_CARD_HAND_TYPE_SCORE
from src.player_hand import PlayerHand
from tests.tests_config import CARDS_DICT, HOLE_CARDS_2_3_SPADES

HI_CARD_9 = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["5_OF_DIAMONDS"],
    card3=CARDS_DICT["7_OF_DIAMONDS"],
    card4=CARDS_DICT["8_OF_SPADES"],
    card5=CARDS_DICT["9_OF_SPADES"],
)

HI_CARD_10_9 = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["5_OF_DIAMONDS"],
    card3=CARDS_DICT["7_OF_DIAMONDS"],
    card4=CARDS_DICT["9_OF_SPADES"],
    card5=CARDS_DICT["10_OF_SPADES"],
)

HI_CARD_10_8 = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["5_OF_DIAMONDS"],
    card3=CARDS_DICT["7_OF_DIAMONDS"],
    card4=CARDS_DICT["8_OF_SPADES"],
    card5=CARDS_DICT["10_OF_SPADES"],
)

HI_CARD_10_8_ALTERNATE = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["5_OF_DIAMONDS"],
    card3=CARDS_DICT["7_OF_DIAMONDS"],
    card4=CARDS_DICT["8_OF_DIAMONDS"],
    card5=CARDS_DICT["10_OF_SPADES"],
)


def test_validate_hi_card(
    hi_card_hand_type_score: int = HI_CARD_HAND_TYPE_SCORE,
):
    valid_cases = [
        HI_CARD_9,
        HI_CARD_10_9,
        HI_CARD_10_8,
        HI_CARD_10_8_ALTERNATE,
    ]

    for community_cards in valid_cases:
        assert (
            PlayerHand(
                hole_cards=HOLE_CARDS_2_3_SPADES,
                community_cards=community_cards,
            ).hand_type.hand_type_score
            == hi_card_hand_type_score
        )


def test_hi_card_tie_breaker():
    community_cards_list = [
        HI_CARD_9,
        HI_CARD_10_9,
        HI_CARD_10_8,
        HI_CARD_10_8_ALTERNATE,
    ]

    hand_types = [
        PlayerHand(
            hole_cards=HOLE_CARDS_2_3_SPADES, community_cards=community_cards
        ).hand_type
        for community_cards in community_cards_list
    ]

    hand_type_scores = [hand_type.hand_type_score for hand_type in hand_types]
    top_ranks = [hand_type.top_ranks[0] for hand_type in hand_types]

    assert all(score == hand_type_scores[0] for score in hand_type_scores)
    assert top_ranks == sorted(top_ranks)

    assert (
        hand_types[community_cards_list.index(HI_CARD_10_8)].top_ranks
        == hand_types[community_cards_list.index(HI_CARD_10_8_ALTERNATE)].top_ranks
    )

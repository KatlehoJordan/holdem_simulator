from src.community_cards import CommunityCards
from src.deck import Deck
from src.player_hand import PlayerHand
from src.straight import STRAIGHT_HAND_TYPE_SCORE
from tests.tests_config import CARDS_DICT, HOLE_CARDS_2_3_SPADES

STRAIGHT_6_HI = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["5_OF_DIAMONDS"],
    card3=CARDS_DICT["6_OF_DIAMONDS"],
    card4=CARDS_DICT["10_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

STRAIGHT_5_HI = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["5_OF_DIAMONDS"],
    card3=CARDS_DICT["9_OF_DIAMONDS"],
    card4=CARDS_DICT["10_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

STRAIGHT_5_HI_ALTERNATE = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["5_OF_DIAMONDS"],
    card3=CARDS_DICT["9_OF_DIAMONDS"],
    card4=CARDS_DICT["10_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)


def test_straight_hand_type_score(
    straight_hand_type_score: int = STRAIGHT_HAND_TYPE_SCORE,
):
    valid_cases = [
        STRAIGHT_6_HI,
        STRAIGHT_5_HI,
        STRAIGHT_5_HI_ALTERNATE,
    ]

    for community_cards in valid_cases:
        assert (
            PlayerHand(
                hole_cards=HOLE_CARDS_2_3_SPADES,
                community_cards=community_cards,
            ).hand_type.hand_type_score
            == straight_hand_type_score
        )


def test_straight_tie_breaker():
    community_cards_list = [
        STRAIGHT_5_HI_ALTERNATE,
        STRAIGHT_5_HI,
        STRAIGHT_6_HI,
    ]

    hand_types = [
        PlayerHand(
            hole_cards=HOLE_CARDS_2_3_SPADES,
            community_cards=community_cards,
        ).hand_type
        for community_cards in community_cards_list
    ]

    hand_type_scores = [hand_type.hand_type_score for hand_type in hand_types]
    top_ranks = [hand_type.top_ranks[0] for hand_type in hand_types]

    assert all(score == hand_type_scores[0] for score in hand_type_scores)
    assert top_ranks == sorted(top_ranks)

    assert (
        hand_types[community_cards_list.index(STRAIGHT_5_HI)].top_ranks
        == hand_types[community_cards_list.index(STRAIGHT_5_HI_ALTERNATE)].top_ranks
    )

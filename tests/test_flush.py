from src.community_cards import CommunityCards
from src.deck import Deck
from src.flush import FLUSH_HAND_TYPE_SCORE
from src.player_hand import PlayerHand
from tests.tests_config import CARDS_DICT, HOLE_CARDS_2_3_SPADES

FLUSH_9_HI_SPADES = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_SPADES"],
    card2=CARDS_DICT["5_OF_SPADES"],
    card3=CARDS_DICT["7_OF_SPADES"],
    card4=CARDS_DICT["8_OF_SPADES"],
    card5=CARDS_DICT["9_OF_SPADES"],
)

FLUSH_9_HI_DIAMONDS = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["5_OF_DIAMONDS"],
    card3=CARDS_DICT["7_OF_DIAMONDS"],
    card4=CARDS_DICT["8_OF_DIAMONDS"],
    card5=CARDS_DICT["9_OF_DIAMONDS"],
)

FLUSH_10_HI_SPADES = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_SPADES"],
    card2=CARDS_DICT["5_OF_SPADES"],
    card3=CARDS_DICT["7_OF_SPADES"],
    card4=CARDS_DICT["8_OF_SPADES"],
    card5=CARDS_DICT["10_OF_SPADES"],
)


def test_flush_hand_type_score(
    flush_hand_type_score: int = FLUSH_HAND_TYPE_SCORE,
) -> None:
    valid_cases = [
        FLUSH_9_HI_SPADES,
        FLUSH_9_HI_DIAMONDS,
        FLUSH_10_HI_SPADES,
    ]

    for community_cards in valid_cases:
        assert (
            PlayerHand(
                hole_cards=HOLE_CARDS_2_3_SPADES,
                community_cards=community_cards,
            ).hand_type.hand_type_score
            == flush_hand_type_score
        )


def test_flush_tie_breakers():
    community_cards_list = [
        FLUSH_9_HI_SPADES,
        FLUSH_9_HI_DIAMONDS,
        FLUSH_10_HI_SPADES,
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
        hand_types[community_cards_list.index(FLUSH_9_HI_SPADES)].top_ranks
        == hand_types[community_cards_list.index(FLUSH_9_HI_DIAMONDS)].top_ranks
    )

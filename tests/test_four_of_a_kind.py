from src.community_cards import CommunityCards
from src.deck import Deck
from src.four_of_a_kind import FourOfAKind
from src.hole_cards import HoleCards
from src.player_hand import PlayerHand
from tests.tests_config import CARDS_DICT, HOLE_CARDS_2_3_SPADES

FOUR_OF_A_KIND_2S = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["2_OF_DIAMONDS"],
    card2=CARDS_DICT["2_OF_HEARTS"],
    card3=CARDS_DICT["2_OF_CLUBS"],
    card4=CARDS_DICT["4_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

FOUR_OF_A_KIND_2S_ALTERNATE = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["2_OF_DIAMONDS"],
    card2=CARDS_DICT["2_OF_HEARTS"],
    card3=CARDS_DICT["2_OF_CLUBS"],
    card4=CARDS_DICT["5_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_DIAMONDS"],
)

FOUR_OF_A_KIND_2S_WEAK_KICKERS = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["2_OF_DIAMONDS"],
    card2=CARDS_DICT["2_OF_HEARTS"],
    card3=CARDS_DICT["2_OF_CLUBS"],
    card4=CARDS_DICT["4_OF_SPADES"],
    card5=CARDS_DICT["4_OF_DIAMONDS"],
)

FOUR_OF_A_KIND_3S = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["3_OF_DIAMONDS"],
    card2=CARDS_DICT["3_OF_HEARTS"],
    card3=CARDS_DICT["3_OF_CLUBS"],
    card4=CARDS_DICT["4_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

FOUR_OF_A_KIND_4S = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["4_OF_DIAMONDS"],
    card2=CARDS_DICT["4_OF_HEARTS"],
    card3=CARDS_DICT["4_OF_CLUBS"],
    card4=CARDS_DICT["4_OF_SPADES"],
    card5=CARDS_DICT["ACE_OF_SPADES"],
)

FOUR_OF_A_KIND_ACES = CommunityCards(
    deck=Deck(),
    card1=CARDS_DICT["ACE_OF_DIAMONDS"],
    card2=CARDS_DICT["ACE_OF_HEARTS"],
    card3=CARDS_DICT["ACE_OF_CLUBS"],
    card4=CARDS_DICT["ACE_OF_SPADES"],
    card5=CARDS_DICT["4_OF_SPADES"],
)


def test_validate_four_of_a_kind():
    test_cases = [
        (FOUR_OF_A_KIND_2S, True),
        (FOUR_OF_A_KIND_2S_ALTERNATE, True),
        (FOUR_OF_A_KIND_2S_WEAK_KICKERS, True),
        (FOUR_OF_A_KIND_3S, True),
        (FOUR_OF_A_KIND_4S, True),
        (FOUR_OF_A_KIND_ACES, True),
    ]

    for community_cards, expected in test_cases:
        assert (
            isinstance(
                PlayerHand(
                    hole_cards=HOLE_CARDS_2_3_SPADES, community_cards=community_cards
                ).hand_type,
                FourOfAKind,
            )
            is expected
        )


def test_four_of_a_kind_winners():
    community_cards_list = [
        FOUR_OF_A_KIND_2S_WEAK_KICKERS,
        FOUR_OF_A_KIND_2S,
        FOUR_OF_A_KIND_2S_ALTERNATE,
        FOUR_OF_A_KIND_3S,
        FOUR_OF_A_KIND_4S,
        FOUR_OF_A_KIND_ACES,
    ]

    hand_types = [
        PlayerHand(
            hole_cards=HOLE_CARDS_2_3_SPADES, community_cards=community_cards
        ).hand_type
        for community_cards in community_cards_list
    ]

    # TODO: Remove type ignoring after finished implementing player_hand with all paths
    hand_type_scores = [hand_type.hand_type_score for hand_type in hand_types]  # type: ignore
    top_ranks = [hand_type.top_ranks[~0] for hand_type in hand_types]  # type: ignore

    assert all(score == hand_type_scores[0] for score in hand_type_scores)
    # TODO: Resolve why this is failing. Consider revising straight, flush, and straight_flush to be sure they are putting everything in the expected order (descending)
    assert top_ranks == sorted(top_ranks)

    assert (
        hand_types[community_cards_list.index(FOUR_OF_A_KIND_2S)].top_ranks  # type: ignore
        == hand_types[
            community_cards_list.index(FOUR_OF_A_KIND_2S_ALTERNATE)
        ].top_ranks  # type: ignore
    )

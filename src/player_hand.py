from src.community_cards import CommunityCards
from src.flush import validate_flush
from src.four_of_a_kind import validate_four_of_a_kind
from src.full_house import validate_full_house
from src.hand_type import HandType
from src.hi_card import validate_hi_card
from src.hole_cards import HoleCards
from src.pair import validate_pair
from src.straight import validate_straight
from src.straight_flush import validate_straight_flush
from src.three_of_a_kind import validate_three_of_a_kind
from src.two_pair import validate_two_pair


class PlayerHand:
    def __init__(self, hole_cards: HoleCards, community_cards: CommunityCards):
        if not isinstance(hole_cards, HoleCards):
            raise ValueError(f"hole_cards must be a HoleCards, not {type(hole_cards)}")
        if not isinstance(community_cards, CommunityCards):
            raise ValueError(
                f"community_cards must be a CommunityCards, not {type(community_cards)}"
            )

        self.cards = [hole_cards.hi_card, hole_cards.lo_card] + community_cards.cards

        validation_functions = [
            validate_straight_flush,
            validate_four_of_a_kind,
            validate_full_house,
            validate_flush,
            validate_straight,
            validate_three_of_a_kind,
            validate_two_pair,
            validate_pair,
            validate_hi_card,
        ]

        for validate in validation_functions:
            hand_found, hand_type_score, top_ranks, name = validate(self.cards)
            print("hand_found:", hand_found)
            print("hand name:", name)
            if hand_found:
                self.hand_type = HandType(
                    hand_type_score=hand_type_score, top_ranks=top_ranks, name=name
                )
                break

    def __str__(self):
        return f"{self.hand_type}"

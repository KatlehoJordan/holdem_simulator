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


# TODO: Will want to extend this so that has some way of capturing hand type == straight flush, and that straight_flush will have attributes: 1) hand_type_score == 8 and 2) high card raw rank value. Next hand type would be == four-of-a-kind with attributes 1) hand_type_score == 7, 2) the raw rank value of the four-of-a-kind and 3) the raw rank value of the kicker. Next hand type would be == full house with attributes 1) hand_type_score == 6, 2) the raw rank value of the three-of-a-kind and 3) the raw rank value of the pair. Next hand type would be == flush with attributes 1) hand_type_score == 5 and 2) the raw rank value of the highest card in the flush, 3) the next highest card in the flush, 4) the third highest card in the flush, 5) the fourth highest card in the flush, and 6) the lowest card in the flush. Next hand type would be == straight with attributes 1) hand_type_score == 4 and 2) the raw rank value of the highest card in the straight. Next hand type would be == three-of-a-kind with attributes 1) hand_type_score == 3, 2) the raw rank value of the three-of-a-kind, 3) the raw rank value of the highest kicker, and 4) the raw rank value of the lowest kicker. Next hand type would be == two-pair with attributes 1) hand_type_score == 2, 2) the raw rank value of the highest pair, 3) the raw rank value of the lowest pair, and 4) the raw rank value of the kicker. Next hand type would be == pair with attributes 1) hand_type_score == 1, 2) the raw rank value of the pair, 3) the raw rank value of the highest kicker, 4) the raw rank value of the second highest kicker, and 5) the raw rank value of the lowest kicker. Next hand type would be == high card with attributes 1) hand_type_score == 0, 2) the raw rank value of the high card, 3) the raw rank value of the second highest card, 4) the raw rank value of the third highest card, 5) the raw rank value of the fourth highest card, and 6) the raw rank value of the lowest card.
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
            # TODO: add validate_two_pair here
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

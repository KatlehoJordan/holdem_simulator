from typing import Union

from src.card import Card
from src.config import logger
from src.scaling_constants import (
    HAND_SHRINK_FACTOR,
    SUBTRACTION_CONSTANT_AFTER_SHRINKING,
)

FLUSH_POTENTIAL_BONUS = 8.0
POCKET_PAIR_BONUS = 66.0
STRAIGHT_POTENTIAL_BONUS_FACTOR = 1.0
NUMBER_OF_CARDS_IN_A_STRAIGHT = 5
ACE_AS_LOW_RAW_RANK_VALUE = 1


class HoleCards:

    def __init__(
        self,
        card1: Union[Card, None] = None,
        card2: Union[Card, None] = None,
        flush_potential_bonus: float = FLUSH_POTENTIAL_BONUS,
        pocket_pair_bonus: float = POCKET_PAIR_BONUS,
        hand_shrink_factor: float = HAND_SHRINK_FACTOR,
        subtraction_constant_after_shrinking: float = SUBTRACTION_CONSTANT_AFTER_SHRINKING,
    ):
        if card1 is None:
            card1 = Card()
        if card2 is None:
            card2 = Card()
        while card1.name == card2.name:
            card2 = Card()
        if not isinstance(card1, Card):
            raise ValueError(f"card1 must be a Card, not {type(card1)}")
        if not isinstance(card2, Card):
            raise ValueError(f"card2 must be a Card, not {type(card2)}")

        self.hi_card, self.lo_card = determine_hi_and_lo_cards(card1, card2)

        self.base_strength = self.hi_card.value + self.lo_card.value

        self.flush_potential_bonus = 0.0
        self.suit_flavor = "off suit"
        if self.hi_card.suit.name == self.lo_card.suit.name:
            self.flush_potential_bonus = flush_potential_bonus
            self.suit_flavor = "suited"

        pocket_pair, self.straight_potential_bonus = (
            determine_pocket_pair_or_straight_potential_bonus(
                self.hi_card, self.lo_card
            )
        )

        if not pocket_pair:
            self.pocket_pair_bonus = 0.0
            self.hand_flavor = (
                f"{self.hi_card.rank}, {self.lo_card.rank} {self.suit_flavor}"
            )
        if pocket_pair:
            self.pocket_pair_bonus = pocket_pair_bonus
            self.hand_flavor = f"Pair of {self.hi_card.rank}s"

        self.summed_value = round(
            self.base_strength
            + self.flush_potential_bonus
            + self.straight_potential_bonus
            + self.pocket_pair_bonus
        )

        self.hole_cards_shrunk_value = self.summed_value * hand_shrink_factor

        self.hole_cards_shrunk_less_constant = (
            self.hole_cards_shrunk_value - subtraction_constant_after_shrinking
        )
        hi_card_message = f"Your hi card is: {self.hi_card.name}"
        lo_card_message = f"Your lo card is: {self.lo_card.name}"
        self.name = f"{hi_card_message}\n{lo_card_message}"
        logger.info("%s", self)

    def __str__(self):
        return f"\n\n{self.name}"

    def show_base_strength(self):
        logger.info("Base strength:")
        logger.info("%s", self.base_strength)

    def show_summed_value(self):
        logger.info("Summed value:")
        logger.info("%s", self.summed_value)

    def show_hi_card_value(self):
        logger.info("Hi card value:")
        logger.info("%s", self.hi_card.value)

    def show_lo_card_value(self):
        logger.info("Lo card value:")
        logger.info("%s", self.lo_card.value)

    def show_pair_bonus(self):
        logger.info("Pair bonus:")
        logger.info("%s", self.pocket_pair_bonus)

    def show_flush_potential_bonus(self):
        logger.info("Flush potential bonus:")
        logger.info("%s", self.flush_potential_bonus)

    def show_straight_potential_bonus(self):
        logger.info("Straight potential bonus:")
        logger.info("%s", self.straight_potential_bonus)


def determine_hi_and_lo_cards(card1: Card, card2: Card) -> tuple[Card, Card]:
    hi_card = card1
    lo_card = card2
    if card1.value > card2.value:
        hi_card = card1
        lo_card = card2
    elif card1.value < card2.value:
        hi_card = card2
        lo_card = card1
    elif card1.value == card2.value:
        if card1.suit.name == card2.suit.name:
            raise ValueError(f"card1 and card2 must be different cards")
        elif card1.suit.name < card2.suit.name:
            hi_card = card1
            lo_card = card2
        elif card1.suit.name > card2.suit.name:
            hi_card = card2
            lo_card = card1
    return hi_card, lo_card


def calculate_straight_potential_bonus(
    rank_diff: int,
    straight_potential_bonus_factor: float = STRAIGHT_POTENTIAL_BONUS_FACTOR,
    number_of_cards_in_a_straight: int = NUMBER_OF_CARDS_IN_A_STRAIGHT,
):
    return straight_potential_bonus_factor * abs(
        rank_diff - number_of_cards_in_a_straight
    )


def determine_pocket_pair_or_straight_potential_bonus(
    hi_card: Card,
    lo_card: Card,
    number_of_cards_in_a_straight: int = NUMBER_OF_CARDS_IN_A_STRAIGHT,
    ace_as_low_raw_rank_value: int = ACE_AS_LOW_RAW_RANK_VALUE,
):
    rank_diff = hi_card.rank.raw_rank_value - lo_card.rank.raw_rank_value
    pocket_pair = False
    straight_potential_bonus = 0.0
    if rank_diff == 0:
        pocket_pair = True
    elif 0 < rank_diff:
        if rank_diff < number_of_cards_in_a_straight:
            straight_potential_bonus = calculate_straight_potential_bonus(rank_diff)
        elif hi_card.rank == "Ace":
            alternative_rank_diff = (
                lo_card.rank.raw_rank_value - ace_as_low_raw_rank_value
            )
            straight_potential_bonus = calculate_straight_potential_bonus(
                alternative_rank_diff
            )
    return pocket_pair, straight_potential_bonus

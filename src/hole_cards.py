import pickle
from pathlib import Path
from typing import Union

from src.card import Card
from src.config import (
    ACE_AS_LOW_RAW_RANK_VALUE,
    DATA_PATH,
    NUMBER_OF_CARDS_IN_QUALIFYING_HAND,
    PICKLE_FILE_SAVE_TYPE,
    RAW_RANK_VALUE_STRING,
    VALID_RANKS_DICT,
    logger,
)
from src.deck import Deck
from src.scaling_constants import (
    HAND_SHRINK_FACTOR,
    SUBTRACTION_CONSTANT_AFTER_SHRINKING,
)

FLUSH_POTENTIAL_BONUS = 8.0
POCKET_PAIR_BONUS = 66.0
STRAIGHT_POTENTIAL_BONUS_FACTOR = 1.0
DEFAULT_WHOSE_CARDS = "Your"
HOLE_CARDS_SUITED_FLAVOR = "suited"
HOLE_CARDS_OFF_SUIT_FLAVOR = "off suit"
HOLE_CARDS_PAIRED_FLAVOR = "s paired"
N_HOLE_CARDS_PER_PLAYER = 2

VALID_HOLE_CARDS_FLAVORS_LIST = []
VALID_HOLE_CARDS_FLAVORS_LIST_FILE_NAME = (
    f"valid_hole_cards_list{PICKLE_FILE_SAVE_TYPE}"
)


class HoleCards:

    def __init__(
        self,
        deck: Deck,
        hole_card_1: Union[Card, None] = None,
        hole_card_2: Union[Card, None] = None,
        whose_cards: str = DEFAULT_WHOSE_CARDS,
    ):
        self.hi_card, self.lo_card = _extract_hi_and_lo_cards(
            deck=deck, card1=hole_card_1, card2=hole_card_2
        )

        (
            self.hole_cards_flavor,
            self.base_strength,
            self.summed_value,
            self.pocket_pair_bonus,
            self.flush_potential_bonus,
            self.straight_potential_bonus,
            self.hole_cards_shrunk_less_constant,
        ) = _find_strength_of_hole_cards(hi_card=self.hi_card, lo_card=self.lo_card)

        self.name = _assign_name(
            hi_card=self.hi_card, lo_card=self.lo_card, whose_cards=whose_cards
        )

    def __str__(self):
        return f"\n{self.name}"

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


def _determine_hi_and_lo_cards(card1: Card, card2: Card) -> tuple[Card, Card]:
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


def _extract_hi_and_lo_cards(
    deck: Deck,
    card1: Union[Card, None] = None,
    card2: Union[Card, None] = None,
) -> tuple[Card, Card]:
    if not isinstance(deck, Deck):
        raise ValueError(f"deck must be a Deck type, not {type(deck)}")
    cards = [card1, card2]
    cards = [card if isinstance(card, Card) else deck.draw_card() for card in cards]

    card_names = [card.name for card in cards]
    for ith_card, card in enumerate(cards):
        while card_names.count(card.name) > 1:
            new_card = deck.draw_card()
            cards[ith_card] = new_card
            card_names[ith_card] = new_card.name

    card1, card2 = cards
    for ith_card, card in enumerate(cards, start=1):
        if not isinstance(card, Card):
            raise ValueError(f"card{ith_card} must be a Card, not {type(card)}")

    hi_card, lo_card = _determine_hi_and_lo_cards(card1, card2)
    return hi_card, lo_card


def _calculate_straight_potential_bonus(
    rank_diff: int,
    straight_potential_bonus_factor: float = STRAIGHT_POTENTIAL_BONUS_FACTOR,
    number_of_cards_in_a_straight: int = NUMBER_OF_CARDS_IN_QUALIFYING_HAND,
) -> float:
    return straight_potential_bonus_factor * abs(
        rank_diff - number_of_cards_in_a_straight
    )


def _determine_pocket_pair_or_straight_potential_bonus(
    hi_card: Card,
    lo_card: Card,
    number_of_cards_in_a_straight: int = NUMBER_OF_CARDS_IN_QUALIFYING_HAND,
    ace_as_low_raw_rank_value: int = ACE_AS_LOW_RAW_RANK_VALUE,
) -> tuple[bool, float]:
    rank_diff = hi_card.rank.raw_rank_value - lo_card.rank.raw_rank_value
    pocket_pair = False
    straight_potential_bonus = 0.0
    if rank_diff == 0:
        pocket_pair = True
    elif 0 < rank_diff:
        if rank_diff < number_of_cards_in_a_straight:
            straight_potential_bonus = _calculate_straight_potential_bonus(rank_diff)
        elif hi_card.rank == "Ace":
            alternative_rank_diff = (
                lo_card.rank.raw_rank_value - ace_as_low_raw_rank_value
            )
            straight_potential_bonus = _calculate_straight_potential_bonus(
                alternative_rank_diff
            )
    return pocket_pair, straight_potential_bonus


def _assign_bonuses_and_hole_cards_flavor(
    hi_card,
    lo_card,
    flush_potential_bonus: float = FLUSH_POTENTIAL_BONUS,
    pocket_pair_bonus: float = POCKET_PAIR_BONUS,
    hole_cards_off_suit_flavor: str = HOLE_CARDS_OFF_SUIT_FLAVOR,
    hole_cards_suited_flavor: str = HOLE_CARDS_SUITED_FLAVOR,
    hole_cards_paired_flavor: str = HOLE_CARDS_PAIRED_FLAVOR,
) -> tuple[float, float, float, str]:
    suit_flavor = hole_cards_off_suit_flavor
    if hi_card.suit.name == lo_card.suit.name:
        suit_flavor = hole_cards_suited_flavor
    else:
        flush_potential_bonus = 0.0

    pocket_pair, straight_potential_bonus = (
        _determine_pocket_pair_or_straight_potential_bonus(hi_card, lo_card)
    )

    hole_cards_flavor = f"{hi_card.rank}{hole_cards_paired_flavor}"
    if not pocket_pair:
        pocket_pair_bonus = 0.0
        hole_cards_flavor = f"{hi_card.rank}, {lo_card.rank} {suit_flavor}"
    return (
        flush_potential_bonus,
        pocket_pair_bonus,
        straight_potential_bonus,
        hole_cards_flavor,
    )


def _find_strength_of_hole_cards(
    hi_card: Card,
    lo_card: Card,
    hand_shrink_factor: float = HAND_SHRINK_FACTOR,
    subtraction_constant_after_shrinking: float = SUBTRACTION_CONSTANT_AFTER_SHRINKING,
) -> tuple[str, float, float, float, float, float, float]:
    base_strength = hi_card.value + lo_card.value

    (
        flush_potential_bonus,
        pocket_pair_bonus,
        straight_potential_bonus,
        hole_cards_flavor,
    ) = _assign_bonuses_and_hole_cards_flavor(hi_card, lo_card)

    summed_value = round(
        base_strength
        + flush_potential_bonus
        + straight_potential_bonus
        + pocket_pair_bonus
    )

    hole_cards_shrunk_value = summed_value * hand_shrink_factor

    hole_cards_shrunk_less_constant = (
        hole_cards_shrunk_value - subtraction_constant_after_shrinking
    )

    return (
        hole_cards_flavor,
        base_strength,
        summed_value,
        pocket_pair_bonus,
        flush_potential_bonus,
        straight_potential_bonus,
        hole_cards_shrunk_less_constant,
    )


def _assign_name(
    hi_card: Card,
    lo_card: Card,
    whose_cards: str = DEFAULT_WHOSE_CARDS,
    default_whose_cards: str = DEFAULT_WHOSE_CARDS,
) -> str:
    hi_card_message = f"{whose_cards} hi card is: {hi_card.name}"
    lo_card_message = f"{whose_cards} lo card is: {lo_card.name}"
    name = f"{hi_card_message}\n{lo_card_message}"
    if whose_cards == default_whose_cards:
        logger.info("%s\n", name)
    else:
        logger.debug("%s\n", name)
    return name


def _make_valid_hole_cards_flavors_list(
    valid_hole_cards_flavors_list: list[str] = VALID_HOLE_CARDS_FLAVORS_LIST,
    valid_ranks_dict: dict[str, dict[str, int]] = VALID_RANKS_DICT,
    raw_rank_value_string: str = RAW_RANK_VALUE_STRING,
    hole_cards_paired_flavor: str = HOLE_CARDS_PAIRED_FLAVOR,
    hole_cards_off_suit_flavor: str = HOLE_CARDS_OFF_SUIT_FLAVOR,
    hole_cards_suited_flavor: str = HOLE_CARDS_SUITED_FLAVOR,
    data_path: Path = DATA_PATH,
    valid_hole_cards_flavors_list_file_name: str = VALID_HOLE_CARDS_FLAVORS_LIST_FILE_NAME,
) -> list[str]:
    pickle_file_path = Path(data_path) / valid_hole_cards_flavors_list_file_name

    if pickle_file_path.exists():
        logger.debug(f"Loading valid hole cards flavors list from {pickle_file_path}")
        with open(pickle_file_path, "rb") as f:
            valid_hole_cards_flavors_list = pickle.load(f)
        return valid_hole_cards_flavors_list
    else:
        logger.info(f"Saving valid hole cards flavors list to {pickle_file_path}")
        valid_hole_cards_flavors_set = set()
        for rank_1 in valid_ranks_dict:
            for rank_2 in valid_ranks_dict:
                if (
                    valid_ranks_dict[rank_1][raw_rank_value_string]
                    < valid_ranks_dict[rank_2][raw_rank_value_string]
                ):
                    continue
                elif rank_1 == rank_2:
                    valid_hole_cards_flavors_set.add(
                        f"{rank_1}{hole_cards_paired_flavor}"
                    )
                else:
                    valid_hole_cards_flavors_set.add(
                        f"{rank_1}, {rank_2} {hole_cards_off_suit_flavor}"
                    )
                    valid_hole_cards_flavors_set.add(
                        f"{rank_1}, {rank_2} {hole_cards_suited_flavor}"
                    )

        valid_hole_cards_flavors_list = sorted(list(valid_hole_cards_flavors_set))
        with open(pickle_file_path, "wb") as f:
            pickle.dump(valid_hole_cards_flavors_list, f)
        return valid_hole_cards_flavors_list


VALID_HOLE_CARDS_FLAVORS_LIST = _make_valid_hole_cards_flavors_list()

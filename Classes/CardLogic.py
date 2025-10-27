from enum import Enum, auto
from .Card import Card, VALUE_RANK
from typing import Tuple, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Cards_Match_Grades(Enum):
    SUIT_EQUAL = auto()
    SUIT_DIFF = auto()

    VALUE_EQUAL = auto()

    VALUE_GREATER = auto()
    VALUE_LESS = auto()


class CardLogic:

    @staticmethod
    def card_is_playble(table_cards: list[Card], card: Card) -> Optional[bool]:

        if not CardLogic.is_card(card):
            return None

        rank = card.get_value_rank

        if rank == 9:
            return True

        suit = card.suit_type

        for card_on_table in table_cards:
            temp_card_suit = card_on_table.suit_type
            if temp_card_suit == suit:

                temp_card_rank = card_on_table.get_value_rank

                diff_temp_to_card = temp_card_rank - rank
                if diff_temp_to_card == 1 or diff_temp_to_card == -1:
                    return True

    @staticmethod
    def is_card(card: Card) -> bool:
        return isinstance(card, Card)

    @staticmethod
    def compare_cards(
        first_card: Card, second_card: Card
    ) -> Optional[Tuple[Cards_Match_Grades, Cards_Match_Grades]]:
        if not CardLogic.is_card(first_card) or not CardLogic.is_card(second_card):
            return None
        else:
            if first_card.suit_type == second_card.suit_type:
                validate_suit = Cards_Match_Grades.SUIT_EQUAL
            else:
                validate_suit = Cards_Match_Grades.SUIT_DIFF

            value_1 = VALUE_RANK[first_card.value]
            value_2 = VALUE_RANK[second_card.value]

            if value_1 == value_2:
                validate_value = Cards_Match_Grades.VALUE_EQUAL
            elif value_1 > value_2:
                validate_value = Cards_Match_Grades.VALUE_GREATER
            else:
                validate_value = Cards_Match_Grades.VALUE_LESS

            if (
                validate_suit == Cards_Match_Grades.SUIT_EQUAL
                and validate_value == Cards_Match_Grades.VALUE_EQUAL
            ):
                raise ValueError("Попытка сравнить карту с самой собой")

            answer = (validate_suit, validate_value)
            return answer

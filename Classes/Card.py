from dataclasses import dataclass
from enum import Enum
from Utils.ColorPrint import cprint

VALUE_RANK = {
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


class Suit_Type(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    SPADES = "♠"
    CLUBS = "♣"


@dataclass(frozen=True)
class Card:
    value: str
    suit_type: Suit_Type

    # def get_suit_type(self) -> str:
    #     return str(self.suit_type.value)
    @property
    def get_value_rank(self) -> int:
        return VALUE_RANK[self.value]

    @property
    def get_str_card(self) -> str:
        if self.value != "10":
            return f"{self.value} {self.suit_type}"
        else:
            return f"{self.value}{self.suit_type}"

    def get_card_color_scheme(self) -> tuple[str, str]:
        """Возвращает пару (цвет_текста, цвет_фона) для карты."""
        bg = "white"
        match self.suit_type:
            case Suit_Type.HEARTS:
                return ("red", bg)
            case Suit_Type.DIAMONDS:
                return ("yellow", bg)
            case Suit_Type.SPADES:
                return ("black", bg)
            case Suit_Type.CLUBS:
                return ("blue", bg)
        return ("black", "white")


def draw_hand_horizontally(hand: list[Card], playable_cards: set[Card]):
    """
    Отображение карт из руки игрока горизонтально
    """
    if not hand:
        return

    card_width = 3

    for i, card in enumerate(hand, start=1):
        card_str = card.get_str_card.ljust(card_width)

        match card.suit_type:
            case "♥":
                cprint(card_str, fg="red", bg="white", end="")
            case "♦":
                cprint(card_str, fg="yellow", bg="white", end="")
            case "♠":
                cprint(card_str, fg="black", bg="white", end="")
            case "♣":
                cprint(card_str, fg="cyan", bg="white", end="")

        if i < len(hand):
            print(" ", end="")

    print()

    for i, card in enumerate(hand, start=1):
        padding_str = " " * card_width
        cprint(padding_str, bg="white", end="")

        if i < len(hand):
            print(" ", end="")
    print("\n")

    for i, card in enumerate(hand, start=1):
        num_str = f"[{i}]".ljust(card_width)
        is_playable = card in playable_cards

        if is_playable:
            cprint(num_str, fg="green", style="bright", end="")
        else:
            cprint(num_str, fg="green", style="dim", end="")

        if i < len(hand):
            print(" ", end="")
    print("\n")

from dataclasses import dataclass, field
from .Card import Card, Suit_Type
import random

@dataclass
class Deck:
    values = ["6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    # labels = [Fore.RED + "♥" + Fore.RESET,
    #             Fore.YELLOW + "♦" + Fore.RESET,
    #             Fore.BLACK + "♠" + Fore.RESET,
    #             Fore.BLUE + "♣"+ Fore.RESET]

    labels = [
        Suit_Type.HEARTS.value,
        Suit_Type.DIAMONDS.value,
        Suit_Type.SPADES.value,
        Suit_Type.CLUBS.value,
    ]

    total_cards: int = 36
    current_cards: int = 36
    cards: list[Card] = field(default_factory=list)

    def set_total_cards(self, total_cards: int):
        total_cards = total_cards

    def __post_init__(self):
        self.fill_deck()

    def fill_deck(self):
        for suit in self.labels:
            for value in self.values:
                new_card = Card(value, suit)
                self.cards.append(new_card)

    def get_x_cards(self, count: int) -> list[Card]:
        num_to_draw = min(count, self.current_cards)

        cards_to_deal = random.sample(self.cards, k=num_to_draw)

        dealt_cards_set = set(cards_to_deal)
        self.cards = [card for card in self.cards if card not in dealt_cards_set]

        self.current_cards = len(self.cards)

        return cards_to_deal

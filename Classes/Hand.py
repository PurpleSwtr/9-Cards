from .Deck import Card, Suit_Type
from .CardLogic import CardLogic
from dataclasses import dataclass, field


@dataclass
class Hand:
    hand: list[Card] = field(default_factory=list)
    activated_turn = None

    def have_card_to_turn(self, cards_on_table):
        cards_unlock = {
            card
            for card in self.hand
            if CardLogic.card_is_playble(table_cards=cards_on_table, card=card)
        }
        if cards_unlock:
            self.activated_turn = True
        else:
            self.activated_turn = False
        return cards_unlock

    def sort_hand(self) -> list[Card]:
        suit_order = {
            Suit_Type.HEARTS.value: 0,
            Suit_Type.DIAMONDS.value: 1,
            Suit_Type.SPADES.value: 2,
            Suit_Type.CLUBS.value: 3,
        }
        self.hand.sort(
            key=lambda card: (suit_order[card.suit_type], card.get_value_rank)
        )

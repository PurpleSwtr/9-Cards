from enum import Enum, auto
from typing import Optional
from pydantic import BaseModel, Field
from .Card import Card, draw_hand_horizontally
from .Hand import Hand
from .Deck import Deck

import random

from Utils.ColorPrint import cprint


class TypePlayer(Enum):
    USER = auto()
    COMPUTER = auto()


class DifficultyAI(Enum):
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()


class PlayerBase(BaseModel):

    player_type: TypePlayer
    name: str = "Игрок"

    turn_order: Optional[int] = None
    money: int = 100
    hand: Hand = Field(default_factory=Hand)

    def add_to_bank(self, bet):
        self.money -= bet
        return bet

    def get_first_card(self, cnt_cards: int, deck: Deck):
        cards_from_deck = deck.get_x_cards(cnt_cards)
        self.hand.hand = cards_from_deck


class UserPlayer(PlayerBase):
    player_type: TypePlayer = Field(default=TypePlayer.USER)

    def init_player(self):
        self.name = input("Введите имя игрока: ")
        ...

    def show_order(self):
        cprint(
            f"Игрок: {self.name} - Ваша очередь хода: {self.turn_order}",
            bg="red",
            fg="yellow",
        )

    def show_cards(self, playable_cards=set[Card]):
        if self.hand.activated_turn:
            color = "green"
            text_card_field = "Карты есть"
        else:
            color = "red"
            text_card_field = "Ходов нет"
        cprint(f"[{' * Ваши карты * ':=^42}]\n", fg=f"{color}")

        draw_hand_horizontally(self.hand.hand, playable_cards)

        text_to_center_2 = f"* {text_card_field} *"
        formatted_line_2 = f"{text_to_center_2:=^44}"
        cprint(f"{formatted_line_2}\n", fg=f"{color}")

    def choose_card(self) -> Optional[Card]:
        user_input = input("Выберите какую карту положить: ")
        try:
            index_from_user = int(user_input)

            if index_from_user <= 0:
                raise IndexError

            return self.hand.hand[index_from_user - 1]
        except ValueError:
            print("Ошибка: Введено не число!")
            return None

        except IndexError:
            print(f"Ошибка: Карты с номером {user_input} не существует!")
            return None


class AIPlayer(PlayerBase):
    player_type: TypePlayer = Field(default=TypePlayer.COMPUTER)
    difficulty: DifficultyAI = Field(default=DifficultyAI.MEDIUM)

    def play_random_card(self, playable_cards: set[Card]) -> Optional[Card]:
        if not playable_cards:
            return None

        chosen_card = random.choice(list(playable_cards))
        return chosen_card

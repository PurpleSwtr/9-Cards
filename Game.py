from Classes.Table import Table

from Classes.Deck import Deck

from Classes.Player import PlayerBase, AIPlayer, UserPlayer, DifficultyAI, TypePlayer

import random
import os
import time

from Utils.ColorPrint import cprint

from dataclasses import dataclass, field


class Config:
    Difficulty: DifficultyAI = DifficultyAI.EASY
    cnt_players: int = 4
    base_player_bank: int = 100
    first_bet: int = 15
    pass_bet: int = 5
    deck_size: int = 36
    user_players_amount: int = 1
    sleep_seconds: int = 3


@dataclass
class Game:
    current_total_turn: int = 0
    current_player: int = 1
    turn_order: list[int] = field(default_factory=list)

    config = Config
    cards_in_hand_cnt: int = int((config.deck_size / config.cnt_players))

    players: list[PlayerBase] = field(default_factory=list)
    ai_players: list[AIPlayer] = field(default_factory=list)
    users_players: list[UserPlayer] = field(default_factory=list)
    bank: int = 0

    def define_turn_orders(self):
        all_cnt = self.config.cnt_players
        player_indices = list(range(1, all_cnt + 1))

        random.shuffle(player_indices)

        self.turn_order = player_indices

    def setup_players(self):
        self.define_turn_orders()

        all_players_cnt = self.config.cnt_players

        for userPlayer in range(self.config.user_players_amount):
            userPlayer = UserPlayer()
            # userPlayer.init_player()
            self.players.append(userPlayer)
            self.users_players.append(userPlayer)

        for ai in range(all_players_cnt - self.config.user_players_amount):
            ai = AIPlayer(difficulty=Config.Difficulty.value)
            self.players.append(ai)
            self.ai_players.append(ai)

        for i, player in enumerate(self.players):

            player.turn_order = self.turn_order[i]

        self.players.sort(key=lambda player: player.turn_order)
        return self.players
        ...


def main():
    game = Game()
    players_list = game.setup_players()

    deck = Deck()
    table = Table()

    deck.set_total_cards(game.config.deck_size)

    for player in players_list:
        player.get_first_card(deck=deck, cnt_cards=game.cards_in_hand_cnt)
        to_bank = player.add_to_bank(bet=game.config.first_bet)
        game.bank += to_bank

    while True:

        for player in players_list:
            os.system("cls" if os.name == "nt" else "clear")
            """
            # Проверка на победу одного из игроков #
            """
            if len(player.hand.hand) > 0:
                # print("Игрок в игре!\n")
                ...

            """ # ОТЛАДКА # """

            table.draw()
            text_to_center_2 = f" Банк: {game.bank} "
            formatted_line_2 = f"{text_to_center_2:=^44}"
            cprint(f"{formatted_line_2}\n", fg="yellow")

            on_table = table.cards_on_table

            for user in game.users_players:
                """# ОТЛАДКА #"""
                user.hand.sort_hand()

                # user.show_order()

                playable_cards = user.hand.have_card_to_turn(cards_on_table=on_table)
                user.show_cards(playable_cards=playable_cards)
                text_to_center_2 = f" Ваши деньги: {user.money} "
                formatted_line_2 = f"{text_to_center_2:=^44}"
                cprint(f"{formatted_line_2}\n", fg="green")

            if player.player_type == TypePlayer.USER:
                if playable_cards:
                    while True:
                        chosen_card = player.choose_card()
                        if chosen_card is None:
                            input("Нажмите Enter для продолжения...")
                            continue
                        elif chosen_card in playable_cards:
                            table.set_card(chosen_card)
                            player.hand.hand.remove(chosen_card)
                            print("Вы выбрали: ", end="")

                            cprint(
                                f"{chosen_card.value} {chosen_card.suit_type}",
                                fg="magenta",
                                style="bright",
                                bg="white",
                            )
                            break
                        else:
                            print(
                                f"Так ходить нельзя! Карта {chosen_card.get_str_card} не подходит."
                            )
                            input("Нажмите Enter для продолжения...")
                else:
                    print("У вас нет ходов! Докладывайте")
                    to_bank = player.add_to_bank(bet=game.config.pass_bet)
                    game.bank += to_bank

            elif player.player_type == TypePlayer.COMPUTER:
                playable_cards = player.hand.have_card_to_turn(cards_on_table=on_table)

                chosen_card = player.play_random_card(playable_cards=playable_cards)

                """ # ОТЛАДКА # """
                if chosen_card:
                    print(f"ИИ-игрок '{player.name}' ходит картой: ", end="")
                    cprint(
                        f"{chosen_card.get_str_card}",
                        fg="magenta",
                        style="bright",
                        bg="white",
                    )
                    table.set_card(chosen_card)
                    player.hand.hand.remove(chosen_card)
                else:
                    print(f"ИИ-игрок '{player.name}' не имеет хода и докладывает.")
                    to_bank = player.add_to_bank(bet=game.config.pass_bet)
                    game.bank += to_bank

            """
            # Проверка на победу одного из игроков #
            """
            if len(player.hand.hand) > 0:
                # print("Игрок в игре!\n")
                ...
            elif len(player.hand.hand) <= 0:
                print("А вот и победитель!!!\n")
                player.money += game.bank

                print(player.player_type)

                print(player)
                return False
            time.sleep(game.config.sleep_seconds)


if __name__ == "__main__":
    main()

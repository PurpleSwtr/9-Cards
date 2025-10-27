from dataclasses import dataclass, field
from typing import Dict, Tuple
from .Card import Card
from Utils.ColorPrint import cprint, format_color


@dataclass
class Table:
    cards_on_table: list[Card] = field(default_factory=list)

    card_positions: Dict[str, Tuple[int, int]] = field(default_factory=dict)

    def __post_init__(self):
        self.init_pos_map()

    def init_pos_map(self):
        suits_order = ["♥", "♦", "♠", "♣"]
        values_order = ["6", "7", "8", "9", "10", "J", "Q", "K", "A"]

        for row_idx, suit in enumerate(suits_order):
            for col_idx, value in enumerate(values_order):
                card_str = f"{value}{suit}" if value == "10" else f"{value} {suit}"
                self.card_positions[card_str] = (row_idx, col_idx)

    def set_card(self, card: Card):
        if card not in self.cards_on_table:
            self.cards_on_table.append(card)

    def draw(self):
        cprint(f"[{' * Стол * ':=^42}]\n", fg="yellow")
        placeholder = "[ ]"
        grid_width = 9
        grid_height = 4
        display_grid: list[list[Card | None]] = [
            [None for _ in range(grid_width)] for _ in range(grid_height)
        ]

        for card in self.cards_on_table:
            pos = self.card_positions.get(card.get_str_card)
            if pos:
                row_idx, col_idx = pos
                if 0 <= row_idx < grid_height and 0 <= col_idx < grid_width:
                    display_grid[row_idx][col_idx] = card

        cell_width = 3
        separator = "  "

        for row in display_grid:
            output_parts = []

            for cell_content in row:
                if isinstance(cell_content, Card):
                    card = cell_content
                    card_str = card.get_str_card.ljust(cell_width)

                    fg_color = ""
                    match card.suit_type:
                        case "♥":
                            fg_color = "red"
                        case "♦":
                            fg_color = "yellow"
                        case "♠":
                            fg_color = "black"
                        case "♣":
                            fg_color = "blue"

                    formatted_part = format_color(card_str, fg=fg_color, bg="white")
                    output_parts.append(formatted_part)
                else:
                    output_parts.append(placeholder.ljust(cell_width))
            print(separator.join(output_parts))
            print()
        cprint(f"[{'':=^42}]", fg="yellow")

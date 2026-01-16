
from typing import TYPE_CHECKING
import tkinter as tk

if TYPE_CHECKING:
    from game import GameController

class Drum:

    def __init__(self, gc: "GameController"):
        self.gc: "GameController" = gc
        
    def display(self, player_number: int, item: str, number: int=None, display_time: int=1250):
        """Display player inventory item for 1 second.
        
        Blocks the calling code but keeps the UI responsive.
        Args:
            item: The inventory item to display (gold, warriors, food, keys, etc.)
        """
        print(f"Displaying {item} for Player {player_number}")
        self.gc.set_player_message(f"Player: {player_number}")

        self.gc.set_message(item)

        if number is not None:
            self.gc.display.set_value(number)

        # Wait 1 second while keeping UI responsive
        wait_var = tk.BooleanVar()
        self.gc.root.after(display_time, wait_var.set, True)
        self.gc.root.wait_variable(wait_var)

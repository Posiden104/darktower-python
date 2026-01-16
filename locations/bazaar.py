"""
Bazaar State

This state represents a player's time at the Bazaar in the game.

"""

from typing import TYPE_CHECKING
from player import Player
from states.player_turn_state import PlayerTurnState

if TYPE_CHECKING:
    from game import GameController


class Bazaar:

    def __init__(self, gc: "GameController"):
        self.gc: "GameController" = gc
        self.display = self.gc.display
        
    def enter(self, state: PlayerTurnState, **kwargs):
        player_number = state.player_number
        self.gc.set_gm_status(f"Player {player_number} is at the bazaar.")
        self.gc.set_player_message(f"Player {player_number}: bazaar.")
        self.player = self.gc.players[player_number - 1]
        self.state:PlayerTurnState = state
        self.set_starting_prices()

    def exit(self):
        self.state.exit_bazaar()

    def set_starting_prices(self):
        """Set the starting prices for bazaar items"""
        self.food_price = 1
        self.warrior_price = self.gc.roll_dice(3) + 5 # 5-8
        self.beast_price = self.gc.roll_dice(9) + 17 # 17-26
        self.scout_price = self.gc.roll_dice(9) + 17 # 17-26
        self.healer_price = self.gc.roll_dice(9) + 17 # 17-26

    def on_button_click(self, text):
        """Handle button clicks"""
        self.gc.set_gm_status("")
        if text == "NO":
            pass
        if text == "YES":
            self.exit()
        if text == "HAGGLE":
            self.gc.set_message("Player Haggled")

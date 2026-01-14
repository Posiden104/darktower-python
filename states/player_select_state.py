"""
Player Select State

This state allows the players to select how many people will play the game.
"""
from typing import TYPE_CHECKING

from states.base_state import State
from player import Player

if TYPE_CHECKING:
    from game import GameController


class PlayerSelectState(State):

    def __init__(self, game_controller: "GameController"):
        super().__init__(game_controller)
        self.game_controller: "GameController" = game_controller
        self.player_count = 1
        
    def enter(self, **kwargs):
        """Set up the player select UI"""
        self.display = self.game_controller.display
        self.display.set_value(self.player_count)
    
    def on_button_click(self, text):
        """Handle button clicks"""
        if text == "NO":
            self.player_count += 1
            if self.player_count > 4:
                self.player_count = 1
            self.display.set_value(self.player_count)
        elif text == "YES":
            self.game_controller.players = [Player(self.game_controller, i) for i in range(self.player_count)]
            self.game_controller.state_machine.change_state("player_turn", player_number=1)

    def exit(self):
        self.game_controller.setup_player_menu()
        pass

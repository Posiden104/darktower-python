"""
Player Select State

This state allows the players to select how many people will play the game.
"""

from states.base_state import State
from inventory import PlayerInventory


class PlayerSelectState(State):

    def __init__(self, game_controller):
        super().__init__(game_controller)
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
            self.game_controller.players = [PlayerInventory() for _ in range(self.player_count)]
            self.game_controller.state_machine.change_state("player_turn", player_number=1)

    def exit(self):
        pass

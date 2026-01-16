"""
Level Select State

This state allows the player to select a difficulty level before starting the game.
"""

from typing import TYPE_CHECKING
from states.base_state import State

if TYPE_CHECKING:
    from game import GameController


class LevelSelectState(State):
    """
    Level selection screen.
    
    Displays options for selecting game difficulty:
    - Level 1 (Easy)
    - Level 2 (Medium)
    - Level 3 (Hard)
    """
    
    def __init__(self, game_controller: "GameController"):
        super().__init__(game_controller)
        self.current_level = 1
        self.gc: "GameController" = game_controller
        self.display = self.gc.display
    
    def enter(self, **kwargs):
        """Set up references to the display"""
        # Show initial level
        self.display.set_value(["l", self.current_level])

        self.gc.set_gm_status(f"Select Level State")

        if self.gc.IS_DEBUG:
            self.current_level = 1
            self.on_button_click("YES")
        
    
    def on_button_click(self, text):
        """Handle button clicks in level select state"""
        # Level selection buttons
        if text == "NO":
            self.current_level += 1
            if self.current_level > 3:
                self.current_level = 1
            self.display.set_value(["l", self.current_level])
        if text == "YES":
            self.gc.state_machine.change_state("player_select")

    def exit(self):
        pass

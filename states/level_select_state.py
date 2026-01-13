"""
Level Select State

This state allows the player to select a difficulty level before starting the game.
"""

from states.base_state import State


class LevelSelectState(State):
    """
    Level selection screen.
    
    Displays options for selecting game difficulty:
    - Level 1 (Easy)
    - Level 2 (Medium)
    - Level 3 (Hard)
    """
    
    def __init__(self, game_controller):
        super().__init__(game_controller)
        self.current_level = 1
    
    def enter(self, **kwargs):
        """Set up references to the display"""
        display = self.game_controller.display
        
        # Show initial level
        display.set_value(["l", self.current_level])

        if self.game_controller.IS_DEBUG:
            self.current_level = 1
            self.on_button_click("YES")
    
    def on_button_click(self, text):
        """Handle button clicks in level select state"""
        display = self.game_controller.display
        
        # Level selection buttons
        if text == "NO":
            self.current_level += 1
            if self.current_level > 3:
                self.current_level = 1
            display.set_value(["l", self.current_level])
        if text == "YES":
            self.game_controller.state_machine.change_state("player_select")

    def exit(self):
        pass

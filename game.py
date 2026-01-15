"""
Dark Tower Game - Main Entry Point

This file serves as the central starting point for the Dark Tower game.
It initializes the window and manages game states through a state machine.
"""

import tkinter as tk
from dragon import Dragon
from drum import Drum
from states.state_machine import StateMachine
from ui.button_grid import ButtonGrid
from ui.seven_segment_display import SevenSegmentDisplay
from ui.player_stats_window import PlayerStatsWindow
from ui.game_master_window import GameMasterWindow
import random

class GameController:
    """
    Main game controller that manages the window and state machine.
    """
    
    def setup_debug(self):
        """Setup debug mode with deterministic random seed"""
        self.random.seed(42)
        self.IS_DEBUG = False

        # Debug steps: list of dicts with 'button' and 'message' keys
        self.debug_steps = [
            {"button": "YES", "message": "Selected Level 1"},
            {"button": "NO", "message": "Selecting 3 players"},
            {"button": "NO", "message": "Selected 3 players"},
            {"button": "YES", "message": "Game started"},
            {"button": "MOVE", "message": "Player 1 moved"}
        ]

        self.grid.disable_all_buttons()
        self.set_message("Executing debug steps...")
        # Start the debug step execution
        self._debug_step_index = 0
        self._execute_next_debug_step()
    
    def _execute_next_debug_step(self):
        """Execute the next debug step with a delay"""
        if self._debug_step_index < len(self.debug_steps):
            step = self.debug_steps[self._debug_step_index]
            button = step["button"]
            message = step.get("message", f"Clicking {button}")  # Default message if not provided
            
            print(f"Step {self._debug_step_index + 1}: {message}")
            self.set_message(message)
            self.grid.on_button_click(button)
            
            # Schedule the next step after 1000ms (1 second)
            self._debug_step_index += 1
            self.root.after(1000, self._execute_next_debug_step)
        else:
            # Re-enable buttons when done
            self.grid.enable_all_buttons()
            print("Debug steps completed!")
            self.set_message("Debug steps completed!")

    
    def create_menu(self):
        """Create the menu bar"""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # File menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        
        file_menu.add_command(label="New Game", command=self.new_game)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Debug Menu
        debug_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Debug", menu=debug_menu)
        debug_menu.add_command(label="Run automated commands", command=self.setup_debug)
        debug_menu.add_command(label="Clear Messages", command=self.clear_message)
        debug_menu.add_separator()
        debug_menu.add_command(label="Set seed 42", command=lambda: self.random.seed(42))


    def setup_player_menu(self):
        """Setup the player menu"""
        # Function menu
        if hasattr(self, 'player_menu_created') and self.player_menu_created:
            self.menubar.delete("Function")
        player_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Function", menu=player_menu)

        for idx, p in enumerate(self.players, start=1):
            m = tk.Menu(player_menu, tearoff=0)
            player_menu.add_cascade(label=f"Player {idx}", menu=m)
            
            # Submenu for each player
            m.add_command(label="Show Gold", command=lambda p=p: p.display("gold"))
            m.add_command(label="Show Warriors", command=lambda p=p: p.display("warriors"))
            m.add_command(label="Show Food", command=lambda p=p: p.display("food"))
            m.add_command(label="Show Keys", command=lambda p=p: p.display("keys"))
        self.player_menu_created = True


    def new_game(self):
        """Start a new game"""
        self.menubar.delete("Function")
        self.player_menu_created = False
        
        # Destroy the player stats window if it exists
        if hasattr(self, 'game_master_window') and self.game_master_window.stats_window:
            self.game_master_window.stats_window.window.destroy()
            self.game_master_window.stats_window = None
        
        self.state_machine.reset()
        self.state_machine.start()



    def __init__(self):
        self.players = []

        self.root = tk.Tk()
        self.root.title("Dark Tower Game")
        self.root.geometry("383x708")
        self.root.configure(bg="black")

        self.random = random.Random()
        # Create menu bar
        self.create_menu()
        
        # DEBUG
        self.IS_DEBUG = True
        self.random.seed(42)
        self.has_forced_move = False
        self.has_forced_die_roll = False
        self.forced_move = ""
        self.forced_die_roll = 0
        
        # Create frame for 7-segment display
        self.display_frame = tk.Frame(self.root, bg="black")
        self.display_frame.pack(pady=(20, 0))
        
        # Create the 7-segment display
        self.display = SevenSegmentDisplay(
            self.display_frame,
            on_color="#d60000",   # Red
            off_color="#2a0000",  # Dark red
            bg_color="#000000"    # Black
        )
        self.display.pack()
        
        # Create message label below display
        self.player_message_label = tk.Label(
            self.root,
            text="",
            bg="black",
            fg="#d60000",  # Red text to match display
            font=("Arial", 10),
            wraplength=350,  # Wrap text to fit window width
            justify=tk.CENTER
        )
        self.player_message_label.pack(pady=(10, 0))

        # Create message label below display
        self.message_label = tk.Label(
            self.root,
            text="",
            bg="black",
            fg="#d60000",  # Red text to match display
            font=("Arial", 10),
            wraplength=350,  # Wrap text to fit window width
            justify=tk.CENTER
        )
        self.message_label.pack(pady=(10, 0))
        
        # Add spacing between message and button grid
        self.spacer_frame = tk.Frame(self.root, bg="black", height=180)
        self.spacer_frame.pack()
        
        # Create frame for button grid
        self.grid_frame = tk.Frame(self.root, bg="black")
        self.grid_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the button grid with callback
        self.grid = ButtonGrid(self.grid_frame, on_button_click_callback=self.on_grid_button_click, game_controller=self)
        
        # Create Drum
        self.drum = Drum(self)

        # Create Dragon
        self.dragon = Dragon(self)

        # Create the game master window
        self.game_master_window = GameMasterWindow(self)

        # Initialize the state machine this enters into an infinite loop of states
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        
    def set_message(self, message):
        """Set the message text below the display"""
        self.message_label.config(text=message)
    
    def set_player_message(self, message):
        """Set the player-specific message text below the display"""
        self.player_message_label.config(text=message)

    def clear_message(self):
        """Clear the message text"""
        self.message_label.config(text="")
        self.player_message_label.config(text="")
    
    def update_stats_display(self):
        """Update the player stats display"""
        if hasattr(self, 'game_master_window') and self.game_master_window.stats_window:
            self.game_master_window.stats_window.update_player_stats()
    
    def on_grid_button_click(self, text):
        """Handle button clicks from the grid"""
        # Delegate to the current state if it has a handler
        if self.state_machine.current_state and hasattr(self.state_machine.current_state, 'on_button_click'):
            self.state_machine.current_state.on_button_click(text)
        else:
            print(f"Button clicked: {text}")
    
    def roll_dice(self):
        """Roll a hex die and return the result"""
        result = self.random.randint(0, 15)
        print(f"Dice rolled: {result}")
        if self.has_forced_die_roll:
            result = self.forced_die_roll
            self.has_forced_die_roll = False
            print(f"Forced die roll applied: {result}")
        return result

    def check_forced_moves(self):
        """Check if there are any forced moves (e.g., from game master)"""
        if self.has_forced_move:
            move = self.forced_move
            self.has_forced_move = False
            print(f"Forced move applied: {move}")
            match move:
                case "lost": return 2
                case "dragon": return 4
                case "plague": return 7
                case "battle": return 10
                case _: return 15 # Nothing
        return None

    def run(self):
        """Start the game loop"""
        self.root.mainloop()

def main():
    game = GameController()
    game.run()


if __name__ == "__main__":
    main()


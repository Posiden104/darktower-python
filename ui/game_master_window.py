"""
Game Master Window - Borderless window for game master controls

Shows game master controls positioned to the right of the main game window.
"""

import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import GameController


class GameMasterWindow:
    """
    Borderless window for game master controls.
    Positioned to the right of the main game window and follows it when moved.
    """

    def __init__(self, game_controller: "GameController"):
        """
        Initialize the game master window.
        
        Args:
            game_controller: Reference to the main game controller
        """
        self.game_controller: "GameController" = game_controller
        self.stats_window = None
        
        # Create the game master window as a Toplevel (child of main window)
        self.window = tk.Toplevel(game_controller.root)
        self.window.geometry("200x400")
        self.window.configure(bg="black")
        self.space_between_windows = 210
        self.stats_window_offset = 620
        
        # Remove title bar and window control buttons
        self.window.overrideredirect(True)
        
        # Position window to the left of the main window
        main_window_x = game_controller.root.winfo_x()
        main_window_y = game_controller.root.winfo_y()
        
        # Position this window to the left (just barely)
        gm_window_x = main_window_x - self.space_between_windows
        gm_window_y = main_window_y
        
        self.window.geometry(f"+{gm_window_x}+{gm_window_y}")
        
        # Bind to main window move events to keep both windows positioned relative to main
        game_controller.root.bind("<Configure>", self._on_main_window_move)
        
        # Title label
        title_label = tk.Label(
            self.window,
            text="Game Master",
            bg="black",
            fg="#d60000",  # Red to match game theme
            font=("Arial", 12, "bold")
        )
        title_label.pack(pady=10)
        
        # Frame to hold buttons
        self.button_frame = tk.Frame(self.window, bg="black")
        self.button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create buttons
        self.create_buttons()
    
    def _on_main_window_move(self, event):
        """Keep both windows positioned relative to main window when it moves"""
        # Only reposition if the event is from the main window being moved
        if event.widget == self.game_controller.root:
            main_window_x = self.game_controller.root.winfo_x()
            main_window_y = self.game_controller.root.winfo_y()
            
            # Position game master window just barely to the left
            gm_window_x = main_window_x - self.space_between_windows
            gm_window_y = main_window_y
            
            self.window.geometry(f"+{gm_window_x}+{gm_window_y}")
            
            # Update stats window position as well
            self._update_stats_window_position()


    def create_buttons(self):
        """Create game master control buttons"""
        
        buttons = {
            "Force Dragon": self.on_force_dragon,
            "Force Plague": self.on_force_plague,
            "Force Lost": self.on_force_lost
        }

        for b in buttons:
            btn = tk.Button(
                self.button_frame,
                text=b,
                bg="#d60000",  # Red
                fg="#ffffff",  # White text
                font=("Arial", 10, "bold"),
                command=buttons[b],
                relief=tk.RAISED,
                padx=10,
                pady=10
            )
            btn.pack(fill=tk.X, pady=5)
    
    def on_force_dragon(self):
        """Handle force dragon button click"""
        print("Force Dragon clicked!")
        # Add game master logic here
        self.game_controller.has_forced_move = True
        self.game_controller.forced_move = "dragon"
            
    def on_force_plague(self):
        """Handle force Plague button click"""
        print("Force Plague clicked!")
        # Add game master logic here
        self.game_controller.has_forced_move = True
        self.game_controller.forced_move = "plague"
            
    def on_force_lost(self):
        """Handle force Lost button click"""
        print("Force Lost clicked!")
        # Add game master logic here
        self.game_controller.has_forced_move = True
        self.game_controller.forced_move = "lost"
    
    def create_stats_window(self):
        """Create the player stats window as a child of this window"""
        if not self.stats_window:
            from ui.player_stats_window import PlayerStatsWindow
            self.stats_window = PlayerStatsWindow(self.game_controller, parent_window=self.window)
            # Position it to the left of game master window
            self._update_stats_window_position()
    
    def _update_stats_window_position(self):
        """Update position of stats window relative to game master window"""
        if self.stats_window:
            gm_x = self.window.winfo_x()
            gm_y = self.window.winfo_y()
            # Position stats window to the right of game master window
            stats_x = gm_x + self.stats_window_offset
            stats_y = gm_y
            self.stats_window.set_position(stats_x, stats_y)
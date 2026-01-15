"""
Player Stats Window - Displays player information in a separate window

Shows each player's gold, warriors, and food in a dedicated stats window
positioned to the left of the main game window.
"""

import tkinter as tk
from tkinter import font as tkfont
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from game import GameController


class PlayerStatsWindow:
    """
    Separate window that displays all players' stats (gold, warriors, food).
    Can be positioned as a child of another window or independently.
    """

    def __init__(self, game_controller: "GameController", parent_window: Optional[tk.Toplevel] = None):
        """
        Initialize the player stats window.
        
        Args:
            game_controller: Reference to the main game controller
            parent_window: Optional parent window to position this within
        """
        self.game_controller = game_controller
        self.players = game_controller.players
        self.parent_window = parent_window
        
        # Create the stats window as a Toplevel (child of parent window or main window)
        if parent_window:
            self.window = tk.Toplevel(parent_window)
        else:
            self.window = tk.Toplevel(game_controller.root)
        
        self.window.title("Player Stats")
        self.window.geometry("300x550")
        self.window.configure(bg="black")
        
        # Remove title bar and window control buttons
        self.window.overrideredirect(True)
        
        # Title label
        title_label = tk.Label(
            self.window,
            text="Player Stats",
            bg="black",
            fg="#d60000",  # Red to match game theme
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=10)
        
        # Frame to hold player stats
        self.stats_frame = tk.Frame(self.window, bg="black")
        self.stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Store player stat labels for updating
        self.player_stat_labels = []
        
        # Create stat displays for each player
        self.create_player_stat_displays()
    
    def create_player_stat_displays(self):
        """Create stat display panels for each player"""
        for idx, player in enumerate(self.players):
            # Player frame
            player_frame = tk.Frame(
                self.stats_frame,
                bg="#1a1a1a",
                relief=tk.SUNKEN,
                borderwidth=2
            )
            player_frame.pack(fill=tk.X, pady=5)
            
            # Player number label
            player_label = tk.Label(
                player_frame,
                text=f"Player {idx + 1}",
                bg="#1a1a1a",
                fg="#f09800",  # Gold color
                font=("Arial", 12, "bold")
            )
            player_label.pack(anchor="w", padx=5, pady=(5, 0))
            
            # Stats container
            stats_container = tk.Frame(player_frame, bg="#1a1a1a")
            stats_container.pack(fill=tk.X, padx=10, pady=5)
            
            # Gold stat
            gold_label = tk.Label(
                stats_container,
                text=f"Gold: {player.gold}",
                bg="#1a1a1a",
                fg="#f09800",
                font=("Arial", 10)
            )
            gold_label.pack(anchor="w")
            
            # Warriors stat
            warriors_label = tk.Label(
                stats_container,
                text=f"Warriors: {player.warriors}",
                bg="#1a1a1a",
                fg="#0090aa",  # Blue
                font=("Arial", 10)
            )
            warriors_label.pack(anchor="w")
            
            # Food stat
            food_label = tk.Label(
                stats_container,
                text=f"Food: {player.food}",
                bg="#1a1a1a",
                fg="#00c100",  # Green
                font=("Arial", 10)
            )
            food_label.pack(anchor="w")
            
            # Store references for updating
            self.player_stat_labels.append({
                'gold': gold_label,
                'warriors': warriors_label,
                'food': food_label
            })
    
    def update_player_stats(self):
        """Update the display with current player stats"""
        for idx, player in enumerate(self.players):
            if idx < len(self.player_stat_labels):
                labels = self.player_stat_labels[idx]
                labels['gold'].config(text=f"Gold: {player.gold}")
                labels['warriors'].config(text=f"Warriors: {player.warriors}")
                labels['food'].config(text=f"Food: {player.food}")
        
        # Refresh the window
        self.window.update_idletasks()
    
    def run(self):
        """Start the stats window event loop"""
        # Don't block the main window - just update when needed
        # The main game loop will call update_player_stats()
        pass
    
    def set_position(self, x: int, y: int):
        """Set the window position"""
        self.window.geometry(f"+{x}+{y}")

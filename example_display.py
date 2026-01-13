"""
Example integration of the 7-segment display with the DarkTower game.

This demonstrates how to add the display to the game window.
You can import and use the display in game.py or run this file standalone.
"""

import tkinter as tk
from ui.seven_segment_display import SevenSegmentDisplay


class GameWithDisplay:
    def __init__(self, root):
        self.root = root
        self.root.title("Dark Tower - 7-Segment Display Example")
        self.root.configure(bg="#000000")
        
        # Create a frame for the display at the top
        display_frame = tk.Frame(root, bg="#000000")
        display_frame.pack(pady=10)
        
        # Create the 7-segment display
        self.display = SevenSegmentDisplay(
            display_frame,
            on_color="#d60000",  # Red (matches game's red_color)
            off_color="#2a0000",  # Dark red
            bg_color="#000000"    # Black
        )
        self.display.pack()
        
        # Create control buttons
        button_frame = tk.Frame(root, bg="#000000")
        button_frame.pack(pady=10)
        
        self.counter = 0
        
        # Decrement button
        btn_dec = tk.Button(
            button_frame, 
            text="- Decrease",
            command=self.decrement,
            font=("Arial", 12),
            bg="#0090aa",  # Blue (matches game's blue_color)
            fg="#ffffff",
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        btn_dec.pack(side=tk.LEFT, padx=5)
        
        # Increment button
        btn_inc = tk.Button(
            button_frame,
            text="+ Increase",
            command=self.increment,
            font=("Arial", 12),
            bg="#00c100",  # Green (matches game's green_color)
            fg="#ffffff",
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        btn_inc.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        btn_reset = tk.Button(
            button_frame,
            text="Reset",
            command=self.reset,
            font=("Arial", 12),
            bg="#c0c0c0",  # Grey (matches game's grey_color)
            fg="#000000",
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        btn_reset.pack(side=tk.LEFT, padx=5)
        
        # Off button
        btn_off = tk.Button(
            button_frame,
            text="Off",
            command=self.turn_off,
            font=("Arial", 12),
            bg="#c0c0c0",  # Grey (matches game's grey_color)
            fg="#000000",
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        btn_off.pack(side=tk.LEFT, padx=5)
        # Initialize display
        self.update_display("off")
    
    def increment(self):
        """Increment the counter."""
        self.counter = (self.counter + 1) % 100
        self.update_display()
    
    def decrement(self):
        """Decrement the counter."""
        self.counter = (self.counter - 1) % 100
        self.update_display()
    
    def reset(self):
        """Reset counter to zero."""
        self.counter = 0
        self.update_display("dash")
    
    def turn_off(self):
        """Turn off the display."""
        self.counter = 0
        self.update_display("off")
    
    def update_display(self, value=None):
        """Update the 7-segment display with current value."""
        if value is None:
            value = self.counter
        self.display.set_value(value)


def main():
    root = tk.Tk()
    app = GameWithDisplay(root)
    root.mainloop()


if __name__ == "__main__":
    main()

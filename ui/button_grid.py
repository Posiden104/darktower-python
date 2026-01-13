import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import GameController

class ButtonGrid:
    """
    A 3x4 grid of colored buttons for the Dark Tower game.
    
    Features:
    - Configuration-driven button creation
    - Support for single and dual-line button text
    - Consistent color palette
    """
    
    def __init__(self, root, on_button_click_callback=None, game_controller:"GameController"=None):
        self.root = root
        self.on_button_click_callback = on_button_click_callback
        self.game_controller:"GameController" = game_controller
        self.buttons_enabled = True
        
        # Color palette
        self.green_color = "#00c100"
        self.grey_color = "#c0c0c0"
        self.red_color = "#d60000"
        self.gold_color = "#f09800"
        self.blue_color = "#0090aa"
        self.white_color = "#ffffff"
        self.orange_color = "#bc5214"
        self.brown_color = "#bb7f37"

        self.root.configure(bg="black")
        
        # Button configuration: Easy to modify!
        # Format: (row, col, text1, text2, color)
        self.button_config = [
            # Row 0
            (0, 0, "YES", "BUY", self.green_color),
            (0, 1, "REPEAT", "", self.grey_color),
            (0, 2, "NO", "END", self.red_color),
            # Row 1
            (1, 0, "HAGGLE", "", self.gold_color),
            (1, 1, "BAZAAR", "", self.blue_color),
            (1, 2, "CLEAR", "", self.white_color),
            # Row 2
            (2, 0, "TOMB", "RUIN", self.blue_color),
            (2, 1, "MOVE", "", self.blue_color),
            (2, 2, "SANCTUARY", "CITADEL", self.blue_color),
            # Row 3
            (3, 0, "DARK TOWER", "", self.orange_color),
            (3, 1, "FRONTIER", "", self.blue_color),
            (3, 2, "INVENTORY", "", self.brown_color),
        ]
        
        self.buttons = {}
        self.create_grid()
    
    def create_grid(self):
        """Create the 3x4 grid of buttons"""
        for row, col, text1, text2, color in self.button_config:
            # Create a frame with black background for the border effect
            outer_frame = tk.Frame(self.root, bg="black")
            outer_frame.grid(row=row, column=col, padx=0, pady=0, sticky="nsew")
            
            # Create the button container
            btn_container = tk.Frame(outer_frame, bg=color, cursor="hand2")
            btn_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
            
            # Bind click event to the container and all its children
            click_cmd = lambda e, t=text1: self.on_button_click(t)
            btn_container.bind("<Button-1>", click_cmd)
            
            if text2:
                # Two-line layout with separator
                # Top half - text anchored to bottom
                top_label = tk.Label(
                    btn_container,
                    text=text1,
                    bg=color,
                    font=("Arial", 12, "bold"),
                    cursor="hand2",
                    pady=0,
                    anchor=tk.S
                )
                top_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                top_label.bind("<Button-1>", click_cmd)
                
                # Separator frame with 10px margins on left and right
                separator_container = tk.Frame(btn_container, bg=color)
                separator_container.pack(side=tk.TOP, fill=tk.X)
                separator = tk.Frame(separator_container, bg="black", height=3)
                separator.pack(fill=tk.X, padx=10)
                separator_container.bind("<Button-1>", click_cmd)
                separator.bind("<Button-1>", click_cmd)
                
                # Bottom half - text anchored to top
                bottom_label = tk.Label(
                    btn_container,
                    text=text2,
                    bg=color,
                    font=("Arial", 12, "bold"),
                    cursor="hand2",
                    pady=0,
                    anchor=tk.N
                )
                bottom_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                bottom_label.bind("<Button-1>", click_cmd)
            else:
                # Single-line layout
                label = tk.Label(
                    btn_container,
                    text=text1,
                    bg=color,
                    font=("Arial", 12, "bold"),
                    cursor="hand2"
                )
                label.pack(fill=tk.BOTH, expand=True)
                label.bind("<Button-1>", click_cmd)
            
            self.buttons[(row, col)] = btn_container
        
        # Configure grid for square, uniform buttons
        for i in range(4):
            self.root.grid_rowconfigure(i, weight=1, uniform="button")
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1, uniform="button")
    
    def on_button_click(self, text):
        """Handle button click events from the grid"""
        if self.buttons_enabled and self.game_controller.IS_DEBUG:
            self.game_controller.clear_message()
        self.handle_button_click(text)
    
    def handle_button_click(self, text):
        """Handle button click events"""
        if self.on_button_click_callback:
            self.on_button_click_callback(text)
        else:
            print(f"Clicked {text} button.")
    
    def set_button_callback(self, row, col, callback):
        """
        Set a custom callback for a specific button.
        
        Args:
            row: Button row (0-3)
            col: Button column (0-2)
            callback: Function to call when button is clicked (takes no arguments)
        """
        container = self.buttons[(row, col)]
        
        # Create new click command
        click_cmd = lambda e: callback()
        
        # Rebind the container and all children
        container.bind("<Button-1>", click_cmd)
        for widget in self._get_all_children(container):
            widget.bind("<Button-1>", click_cmd)
    
    def _get_all_children(self, widget):
        """Recursively get all child widgets"""
        children = []
        for child in widget.winfo_children():
            children.append(child)
            children.extend(self._get_all_children(child))
        return children
    
    def disable_all_buttons(self):
        """Disable all buttons in the grid"""
        self.buttons_enabled = False
        for container in self.buttons.values():
            container.unbind("<Button-1>")
            container.configure(cursor="")
            for widget in self._get_all_children(container):
                widget.unbind("<Button-1>")
                if isinstance(widget, tk.Label):
                    widget.configure(cursor="")
    
    def enable_all_buttons(self):
        """Enable all buttons in the grid"""
        self.buttons_enabled = True
        for (row, col), container in self.buttons.items():
            # Find the text for this button
            text1 = self.button_config[row * 3 + col][2]
            click_cmd = lambda e, t=text1: self.on_button_click(t)
            
            container.bind("<Button-1>", click_cmd)
            container.configure(cursor="hand2")
            for widget in self._get_all_children(container):
                widget.bind("<Button-1>", click_cmd)
                if isinstance(widget, tk.Label):
                    widget.configure(cursor="hand2")
    
    def disable_button(self, text):
        """
        Disable a specific button by its text label.
        
        Args:
            text: The text label of the button to disable (e.g., "MOVE", "YES")
        """
        for (row, col), container in self.buttons.items():
            btn_text = self.button_config[row * 3 + col][2]
            if btn_text == text:
                container.unbind("<Button-1>")
                container.configure(cursor="")
                for widget in self._get_all_children(container):
                    widget.unbind("<Button-1>")
                    if isinstance(widget, tk.Label):
                        widget.configure(cursor="")
                break
    
    def enable_button(self, text):
        """
        Enable a specific button by its text label.
        
        Args:
            text: The text label of the button to enable (e.g., "MOVE", "YES")
        """
        for (row, col), container in self.buttons.items():
            btn_text = self.button_config[row * 3 + col][2]
            if btn_text == text:
                click_cmd = lambda e, t=text: self.on_button_click(t)
                container.bind("<Button-1>", click_cmd)
                container.configure(cursor="hand2")
                for widget in self._get_all_children(container):
                    widget.bind("<Button-1>", click_cmd)
                    if isinstance(widget, tk.Label):
                        widget.configure(cursor="hand2")
                break

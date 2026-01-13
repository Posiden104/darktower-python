import tkinter as tk
from tkinter import Canvas


class SevenSegmentDisplay:
    """
    A 2-digit 7-segment LED-style display component for Tkinter.
    
    Segments are labeled:
         aaa
        f   b
        f   b
         ggg
        e   c
        e   c
         ddd
    
    Usage:
        display = SevenSegmentDisplay(parent, width=200, height=100)
        display.pack()
        display.set_value(42)  # Display "42"
        display.set_value(7)   # Display "07" (leading zero)
    """
    
    # Segment patterns for each digit (0-9)
    # Each bit represents: a, b, c, d, e, f, g
    DIGIT_SEGMENTS = {
        0: [1, 1, 1, 1, 1, 1, 0],  # 0
        1: [0, 1, 1, 0, 0, 0, 0],  # 1
        2: [1, 1, 0, 1, 1, 0, 1],  # 2
        3: [1, 1, 1, 1, 0, 0, 1],  # 3
        4: [0, 1, 1, 0, 0, 1, 1],  # 4
        5: [1, 0, 1, 1, 0, 1, 1],  # 5
        6: [1, 0, 1, 1, 1, 1, 1],  # 6
        7: [1, 1, 1, 0, 0, 0, 0],  # 7
        8: [1, 1, 1, 1, 1, 1, 1],  # 8
        9: [1, 1, 1, 1, 0, 1, 1],  # 9
        "dash": [0, 0, 0, 0, 0, 0, 1],  # -
        "minus": [0, 0, 0, 0, 0, 0, 1],  # -
        "-": [0, 0, 0, 0, 0, 0, 1],  # -
        "off": [0, 0, 0, 0, 0, 0, 0],  # all segments off
        "l": [0, 0, 0, 1, 1, 1, 0]  # L
    }
    
    def __init__(self, parent, on_color="#d60000", off_color="#2a0000", bg_color="#000000"):
        """
        Initialize the 2-digit 7-segment display.
        
        Args:
            parent: Parent Tkinter widget
            on_color: Color for lit segments (default: red)
            off_color: Color for unlit segments (default: dark red)
            bg_color: Background color (default: black)
        """
        self.parent = parent
        self.width = 120
        self.height = 100
        self.on_color = on_color
        self.off_color = off_color
        self.bg_color = bg_color
        
        # Create canvas
        self.canvas = Canvas(parent, width=self.width, height=self.height, 
                           bg=bg_color, highlightthickness=0)
        
        # Calculate dimensions for each digit
        self.digit_width = self.width // 2 - 3  # Space for 2 digits with minimal padding
        self.digit_height = self.height - 6
        self.segment_thickness = max(5, min(self.digit_width, self.digit_height) // 10)
        
        # Store segment IDs for each digit
        self.digit1_segments = []
        self.digit2_segments = []
        
        # Create the segments for both digits
        self._create_digit(0, self.digit1_segments)
        self._create_digit(1, self.digit2_segments)
        
        # Initialize to off
        self.set_value("off")
    
    def _create_digit(self, digit_index, segment_list):
        """
        Create the 7 segments for a single digit.
        
        Args:
            digit_index: 0 for left digit, 1 for right digit
            segment_list: List to store segment IDs
        """
        x_offset = 3 + digit_index * (self.digit_width + 6)
        y_offset = 5
        
        w = self.digit_width
        h = self.digit_height
        t = self.segment_thickness
        
        # Calculate segment dimensions - horizontal width = vertical height
        segment_height = h // 2  # Height of each vertical segment
        segment_width = segment_height  # Width of horizontal segments matches vertical height
        
        # Define segment coordinates (relative to digit position)
        # Segment a (top)
        seg_a = self._create_horizontal_segment(x_offset, y_offset, segment_width)
        
        # Segment b (top-right)
        seg_b = self._create_vertical_segment(x_offset + segment_width - t, y_offset, segment_height)
        
        # Segment c (bottom-right)
        seg_c = self._create_vertical_segment(x_offset + segment_width - t, y_offset + segment_height, segment_height)
        
        # Segment d (bottom)
        seg_d = self._create_horizontal_segment(x_offset, y_offset + h - t, segment_width)
        
        # Segment e (bottom-left)
        seg_e = self._create_vertical_segment(x_offset, y_offset + segment_height, segment_height)
        
        # Segment f (top-left)
        seg_f = self._create_vertical_segment(x_offset, y_offset, segment_height)
        
        # Segment g (middle)
        seg_g = self._create_horizontal_segment(x_offset, y_offset + segment_height - t // 2, segment_width)
        
        # Store in order: a, b, c, d, e, f, g
        segment_list.extend([seg_a, seg_b, seg_c, seg_d, seg_e, seg_f, seg_g])
    
    def _create_horizontal_segment(self, x, y, width):
        """Create a horizontal segment (trapezoid shape)."""
        t = self.segment_thickness
        points = [
            x + t, y,
            x + width - t, y,
            x + width, y + t,
            x, y + t
        ]
        return self.canvas.create_polygon(points, fill=self.off_color, outline="")
    
    def _create_vertical_segment(self, x, y, height):
        """Create a vertical segment (trapezoid shape)."""
        t = self.segment_thickness
        points = [
            x, y + t,
            x + t, y,
            x + t, y + height - t,
            x, y + height
        ]
        return self.canvas.create_polygon(points, fill=self.off_color, outline="")
    
    def _update_digit(self, digit_segments, digit_value):
        """
        Update a single digit's segments.
        
        Args:
            digit_segments: List of segment IDs for this digit
            digit_value: Integer value (0-9) to display or special values "dash", "off", "minus"
        """
        if digit_value not in self.DIGIT_SEGMENTS:
            digit_value = 0
        
        pattern = self.DIGIT_SEGMENTS[digit_value]
        
        for i, segment_id in enumerate(digit_segments):
            color = self.on_color if pattern[i] else self.off_color
            self.canvas.itemconfig(segment_id, fill=color)
    
    def set_value(self, value):
        """
        Set the display value (-9 to 99) or set each digit individually.
        
        Args:
            value: Integer value to display (will be clamped to -9 to 99),
                   string command ("dash", "off", "minus"), or
                   array/list of 2 items [digit1, digit2] where each can be 0-9, "dash", "minus", or "off"
        """
        
        # Check if value is an array of 2 items
        if isinstance(value, (list, tuple)) and len(value) == 2:
            self._update_digit(self.digit1_segments, value[0])
            self._update_digit(self.digit2_segments, value[1])
            return

        if value == "dash":
            self._update_digit(self.digit1_segments, "dash")
            self._update_digit(self.digit2_segments, "dash")
            return
        if value == "off":
            self._update_digit(self.digit1_segments, "off")
            self._update_digit(self.digit2_segments, "off")
            return
        if value == "minus":
            self._update_digit(self.digit1_segments, "minus")
            self._update_digit(self.digit2_segments, "off")
            return
        
        # Clamp value to -9 to 99
        value = max(-9, min(99, int(value)))
        
        # Handle negative numbers
        if value < 0:
            self._update_digit(self.digit1_segments, "minus")
            self._update_digit(self.digit2_segments, abs(value))
        # Handle 0-9 (show leading space)
        elif value < 10:
            self._update_digit(self.digit1_segments, "off")
            self._update_digit(self.digit2_segments, value)
        # Handle 10-99 (show both digits)
        else:
            tens = value // 10
            ones = value % 10
            self._update_digit(self.digit1_segments, tens)
            self._update_digit(self.digit2_segments, ones)
    
    def pack(self, **kwargs):
        """Pack the display canvas."""
        self.canvas.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the display canvas."""
        self.canvas.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place the display canvas."""
        self.canvas.place(**kwargs)

    def clear(self):
        """Clear the display (turn off all segments)."""
        self._update_digit(self.digit1_segments, "off")
        self._update_digit(self.digit2_segments, "off")

if __name__ == "__main__":
    # Demo/test code
    root = tk.Tk()
    root.title("7-Segment Display Demo")
    root.geometry("400x300")
    root.configure(bg="#000000")
    
    # Create display
    display = SevenSegmentDisplay(root, on_color="#d60000", off_color="#2a0000")
    display.pack(pady=20)
    
    # Create controls
    control_frame = tk.Frame(root, bg="#000000")
    control_frame.pack(pady=10)
    
    current_value = [0]
    
    def increment():
        current_value[0] = (current_value[0] + 1) % 100
        display.set_value(current_value[0])
        value_label.config(text=f"Value: {current_value[0]:02d}")
    
    def decrement():
        current_value[0] = (current_value[0] - 1) % 100
        display.set_value(current_value[0])
        value_label.config(text=f"Value: {current_value[0]:02d}")
    
    btn_dec = tk.Button(control_frame, text="-", command=decrement, 
                       font=("Arial", 16), width=3)
    btn_dec.pack(side=tk.LEFT, padx=5)
    
    value_label = tk.Label(control_frame, text="Value: 00", 
                          font=("Arial", 12), bg="#000000", fg="#ffffff")
    value_label.pack(side=tk.LEFT, padx=10)
    
    btn_inc = tk.Button(control_frame, text="+", command=increment, 
                       font=("Arial", 16), width=3)
    btn_inc.pack(side=tk.LEFT, padx=5)
    
    # Second row of controls
    control_frame2 = tk.Frame(root, bg="#000000")
    control_frame2.pack(pady=5)
    
    btn_off = tk.Button(control_frame2, text="Off", command=lambda: display.set_value("off"), 
                       font=("Arial", 16), width=3)
    btn_off.pack(side=tk.LEFT, padx=5)

    btn_dash = tk.Button(control_frame2, text="Dash", command=lambda: display.set_value("dash"), 
                       font=("Arial", 16), width=4)
    btn_dash.pack(side=tk.LEFT, padx=5)

    root.mainloop()

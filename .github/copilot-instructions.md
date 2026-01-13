# DarkTower AI Agent Instructions

## Project Overview
Tkinter GUI game with a 3x4 grid of colored buttons. Currently implemented as a single file ([game.py](game.py)), but **should be refactored into multiple modules as features are added**.

## Architecture Pattern
- **Multi-file organization**: Create separate files for distinct concerns as the codebase grows
  - `game.py`: Main entry point and game orchestration
  - `ui/`: UI components (grid, buttons, dialogs)
  - `models/`: Game state, logic, and data structures
  - `config.py` or `constants.py`: Shared configuration and color palette
- **Configuration-driven buttons**: The `button_config` list defines the grid layout - modify this list rather than hardcoding individual button creation
- **Dictionary-based button storage**: Buttons are indexed by `(row, col)` tuples for efficient access

## Key Color Palette
Consistent color scheme defined as class attributes (lines 10-17):
- Green: `#00c100`, Grey: `#c0c0c0`, Red: `#d60000`
- Gold: `#f09800`, Blue: `#0090aa`, White: `#ffffff`
- Orange: `#bc5214`, Brown: `#bb7f37`

Always use these named attributes (`self.green_color`, etc.) rather than hardcoding hex values.

## Grid Layout Convention
- **3 columns × 4 rows** (12 buttons total)
- Black borders created using frame padding
- Buttons expand to fill available space via grid weights

## Modifying Buttons
**Pattern**: Modify the `button_config` list in ButtonGrid class to change button layout:
```python
self.button_config = [
    (row, col, text1, text2, color),
    # Example:
    (0, 0, "YES", "BUY", self.green_color),
]
```

## Code Organization Guidelines
- **Create new files proactively**: When adding features (game state, sound, animations, AI), create dedicated modules instead of extending [game.py](game.py)
- **Import pattern**: Keep [game.py](game.py) as the entry point that imports and coordinates other modules
- **Example structure for new features**:
  ```
  game.py              # Main entry point
  constants.py         # Colors, dimensions, configuration
  ui/grid.py          # ButtonGridGame class
  models/game_state.py # Game logic and state management
  utils/helpers.py     # Shared utilities
  ```

## Running & Debugging
- **Run**: Execute `python game.py` from project root
- **Debug**: Use VS Code's "Python Debugger: Current File" configuration (F5)
- **Entry point**: `main()` function (lines 82-85)

## UI Specifications
- Window size: 404×505px (line 8)
- Button style: Flat with no borders (`relief=tk.FLAT, borderwidth=0`)
- Font: Arial 12pt (line 53)
- Button dimensions: 12 width × 3 height (lines 54-55)

## Event Handling
Click events route through `on_button_click(row, col)` (lines 71-73). Currently prints to console - extend this method for game logic.

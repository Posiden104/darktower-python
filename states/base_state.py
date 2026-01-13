"""
Base State Class

This is the abstract base class for all game states in Dark Tower.
Each state is responsible for setting up its own UI and handling transitions.
"""

from abc import ABC, abstractmethod


class State(ABC):
    """
    Abstract base class for game states.
    
    Each state should:
    1. Initialize its UI components in __init__
    2. Clean up resources in cleanup()
    3. Define transitions in get_transitions()
    """
    
    def __init__(self, game_controller):
        """
        Initialize the state.
        
        Args:
            game_controller: Reference to the main game controller with root window
        """
        self.game_controller = game_controller
        self.root = game_controller.root
    
    @abstractmethod
    def enter(self):
        """
        Called when entering this state.
        Set up UI components and initial state here.
        """
        pass
    
    @abstractmethod
    def exit(self):
        """
        Called when exiting this state.
        Clean up UI components here.
        """
        pass
    
    def update(self):
        """
        Called periodically to update the state (optional).
        Override if the state needs periodic updates.
        """
        pass

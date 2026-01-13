"""
State Machine Manager

Manages state transitions and the current active state for the Dark Tower game.
"""


from states.level_select_state import LevelSelectState
from states.player_select_state import PlayerSelectState
from states.player_turn_state import PlayerTurnState


class StateMachine:
    """
    Manages game states and handles transitions between them.
    
    Usage:
        state_machine = StateMachine(game_controller)
        state_machine.register_state("level_select", LevelSelectState)
        state_machine.register_state("game_play", GamePlayState)
        state_machine.change_state("level_select")
    """
    
    def __init__(self, game_controller):
        """
        Initialize the state machine.
        
        Args:
            game_controller: Reference to the main game controller
        """
        self.game_controller = game_controller
        self.states = {}  # Dictionary of state_name -> State class
        self.current_state = None
        self.current_state_name = None
    
    def register_state(self, state_name, state_class):
        """
        Register a state class with the state machine.
        
        Args:
            state_name: Unique identifier for the state
            state_class: The State class (not instance) to register
        """
        self.states[state_name] = state_class
    
    def change_state(self, new_state_name, **kwargs):
        """
        Transition to a new state.
        
        Args:
            new_state_name: Name of the state to transition to
            *args: Positional arguments to pass to the state's enter() method
            **kwargs: Keyword arguments to pass to the state's enter() method
        """
        if new_state_name not in self.states:
            raise ValueError(f"State '{new_state_name}' not registered")
        
        # Exit current state if one exists
        if self.current_state:
            self.current_state.exit()
        
        # Create and enter new state
        state_class = self.states[new_state_name]
        self.current_state = state_class(self.game_controller)
        self.current_state_name = new_state_name
        self.current_state.enter(**kwargs)
    
    def update(self):
        """
        Update the current state (call periodically if needed).
        """
        if self.current_state:
            self.current_state.update()
    
    def get_current_state_name(self):
        """
        Get the name of the current state.
        
        Returns:
            Current state name or None
        """
        return self.current_state_name

    def reset(self):
        """
        Reset the state machine to its initial state.
        Exits the current state and clears all state references.
        """
        # Exit current state if one exists
        if self.current_state:
            self.current_state.exit()
        
        # Clear current state references
        self.current_state = None
        self.current_state_name = None

        self.states.clear()

    def start(self):
        """
        Start the state machine by registering all states and transitioning to the initial state.
        """

        if len(self.states) == 0:
            # Register all game states
            self.register_state("level_select", LevelSelectState)
            self.register_state("player_select", PlayerSelectState)
            self.register_state("player_turn", PlayerTurnState)
        else:
            raise ValueError(f"State Machine start method called when states are already registered: {list(self.states.keys())}")
        
        # Start with level select state
        self.change_state("level_select")

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import GameController

class Dragon:

    def __init__(self, gc: "GameController"):
        self.gold = 0
        self.warriors = 0
    
    
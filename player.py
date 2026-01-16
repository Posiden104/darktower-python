
from typing import TYPE_CHECKING
import tkinter as tk

if TYPE_CHECKING:
    from game import GameController

class Player:

    def __init__(self, gc: "GameController", player_number: int):
        self.warriors = 10
        self.gold = 30
        self.food = 25
        self.bronze_key = False
        self.silver_key = False
        self.gold_key = False
        self.dragon_sword = False
        self.beast = False
        self.healer = False
        self.pegasus = False
        self.kingdom = 1
        self.gc: "GameController" = gc
        self.player_number = player_number + 1

    def can_enter_frontier(self) -> bool:
        match self.kingdom:
            case 1:
                return self.bronze_key and not self.gold_key
            case 2:
                return self.silver_key
            case 3:
                return self.gold_key
    
    def consume_food(self):
        if self.warriors <= 15:
            self.food -= 1
        elif self.warriors <= 30:
            self.food -= 2
        elif self.warriors <= 45:
            self.food -= 3
        elif self.warriors <= 60:
            self.food -= 4
        elif self.warriors <= 75:
            self.food -= 5
        elif self.warriors <= 90:
            self.food -= 6
        elif self.warriors <= 99:
            self.food -= 7
    
    def get_plagued(self):
        print(f"Player {self.player_number} has been plagued!")
        self.gc.set_gm_status(f"Player {self.player_number} has been plagued!")
        self.gc.drum.display(self.player_number, "plague")
        
        if self.healer:
            self.gc.drum.display(self.player_number, "healer")
            self.warriors += 2
        else:
            self.warriors -= 2
        
        self.warriors = max(0, self.warriors)
        self.warriors = min(99, self.warriors)
        
        self.gc.drum.display(self.player_number, "warriors", self.warriors)

    def get_lost(self):
        print(f"Player {self.player_number} has gotten lost!")
        self.gc.drum.display(self.player_number, "lost")

    def dragon_attack(self):
        self.gc.set_gm_status(f"Player {self.player_number} is being attacked by the dragon!")
        
        if self.dragon_sword:
            print(f"Player {self.player_number} used the Dragon Sword to defeat the dragon!")
            self.gc.drum.display(self.player_number, "dragon_sword")

            self.warriors += self.gc.dragon.warriors
            self.gc.dragon.warriors = 0
            self.gc.drum.display(self.player_number, "warriors", self.warriors)

            self.gold += self.gc.dragon.gold
            self.gc.dragon.gold = 0
            self.gc.drum.display(self.player_number, "gold", self.gold)

        else:
            def calculate_loss(value) -> int:
                lost_value = 0
                value_ones = value % 10
                value_tens = (value // 10) % 10
                # Start the calculation based on the original value in the 1s digit
                #
                # 0-3 becomes 0
                # 4-7 becomes 1
                # 8-9 becomes 3

                if value_ones < 4:
                    lost_value += 0
                elif value_ones < 7:
                    lost_value += 1
                elif value_ones < 9:
                    lost_value += 3
                
                # Now, check the original 10s digit
                #
                # 1 (10-19 originally) adds 2 to 1s digit
                # 2 (20-29 originally) adds 5 to 1s digit
                if value_tens == 1:
                    lost_value += 2
                elif value_tens == 2:
                    lost_value += 5
                
                # Now, tweak the 10s digit the same way the 1s digit was tweaked originally
                #
                # 0-3 becomes 0
                # 4-7 becomes 1
                # 8-9 becomes 3

                if value_tens < 4:
                    lost_value += 0
                elif value_tens < 7:
                    lost_value += 10
                elif value_tens < 9:
                    lost_value += 30
                
                # Finally, ensure we don't take more than we have
                return min(lost_value, value)

            lost_gold = calculate_loss(self.gold)
            lost_warriors = calculate_loss(self.warriors)
            
            self.gold = self.gold - lost_gold
            self.warriors = self.warriors - lost_warriors

            self.gc.dragon.gold += lost_gold
            self.gc.dragon.warriors += lost_warriors

            self.gc.drum.display(self.player_number, "dragon")
            self.gc.drum.display(self.player_number, "gold", self.gold)
            self.gc.drum.display(self.player_number, "warriors", self.warriors)
    
    def add_key(self):
        if self.kingdom == 2 and not self.bronze_key:
            self.bronze_key = True
            self.gc.drum.display(self.player_number, "Bronze Key")
        elif self.kingdom == 3 and not self.silver_key:
            self.silver_key = True
            self.gc.drum.display(self.player_number, "Silver Key")
        elif self.kingdom == 4 and not self.gold_key:
            self.gold_key = True
            self.gc.drum.display(self.player_number, "Gold Key")
    
    def add_dragon_sword(self):
        self.dragon_sword = True
    
    def add_beast(self):
        self.beast = True
    
    def add_healer(self):
        self.healer = True
    
    def add_pegasus(self):
        self.pegasus = True
    
    def add_wizard(self):
        self.gc.set_message(f"Player {self.player_number} has acquired the Wizard!")
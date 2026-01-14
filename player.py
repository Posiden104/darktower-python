
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import GameController

class Player:

    def __init__(self, game_controller: "GameController", player_number: int):
        self.warriors = 10
        self.gold = 30
        self.food = 25
        self.bronze_key = False
        self.silver_key = False
        self.gold_key = False
        self.dragon_sword = False
        self.beast = False
        self.healer = False
        self.kingdom = 1
        self.game_controller: "GameController" = game_controller
        self.player_number = player_number + 1

    def can_enter_frontier(self) -> bool:
        match self.kingdom:
            case 1:
                return self.bronze_key and not self.gold_key
            case 2:
                return self.silver_key
            case 3:
                return self.gold_key
    
    def display(self, item):
        self.game_controller.set_player_message(f"Player: {self.player_number}")

        match item:
            case "gold":
                self.game_controller.set_message(f"Gold: {self.gold}")
                return f"Gold: {self.gold}"
            case "warriors":
                self.game_controller.set_message(f"Warriors: {self.warriors}")
                return f"Warriors: {self.warriors}"
            case "food":
                self.game_controller.set_message(f"Food: {self.food}")
                return f"Food: {self.food}"
            case "keys":
                keys = []
                if self.bronze_key:
                    keys.append("Bronze Key")
                if self.silver_key:
                    keys.append("Silver Key")
                if self.gold_key:
                    keys.append("Gold Key")
                self.game_controller.set_message("Keys: " + ", ".join(keys) if keys else "No Keys")
                return "Keys: " + ", ".join(keys) if keys else "No Keys"
            case "beast":
                self.game_controller.set_message(f"Beast: {'Yes' if self.beast else 'No'}")
                return f"Beast: {'Yes' if self.beast else 'No'}"
            case "healer":
                self.game_controller.set_message(f"Healer: {'Yes' if self.healer else 'No'}")
                return f"Healer: {'Yes' if self.healer else 'No'}"
            case "dragon_sword":
                self.game_controller.set_message(f"Dragon Sword: {'Yes' if self.dragon_sword else 'No'}")
                return f"Dragon Sword: {'Yes' if self.dragon_sword else 'No'}"
            case _:
                return "Unknown item"

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
    
    def dragon_attack(self):
        if self.dragon_sword:
            self.game_controller.set_message(f"Player {self.player_number} used the Dragon Sword to defeat the dragon!")
            return True
        else:
            gold_ones = self.gold % 10
            gold_tens = (self.gold // 10) % 10
            warriors_ones = self.warriors % 10
            warriors_tens = (self.warriors // 10) % 10

            lost_gold = 0
            lost_warriors = 0

            def calculate_loss(value_ones, value_tens) -> int:
                lost_value = 0
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
                
                return lost_value

            lost_gold = calculate_loss(gold_ones, gold_tens)
            lost_warriors = calculate_loss(warriors_ones, warriors_tens)

            self.gold = max(0, self.gold - lost_gold)
            self.warriors = max(0, self.warriors - lost_warriors)
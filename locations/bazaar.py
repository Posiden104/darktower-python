"""
Bazaar State

This state represents a player's time at the Bazaar in the game.

"""

from typing import TYPE_CHECKING
from player import Player
from states.player_turn_state import PlayerTurnState

if TYPE_CHECKING:
    from game import GameController


class Bazaar:

    def __init__(self, gc: "GameController"):
        self.gc: "GameController" = gc
        self.display = self.gc.display
        
    def enter(self, state: PlayerTurnState, **kwargs):
        player_number = state.player_number
        self.gc.set_gm_status(f"Player {player_number} is at the bazaar.")
        self.gc.set_player_message(f"Player {player_number}: bazaar.")
        self.player = self.gc.players[player_number - 1]
        self.state:PlayerTurnState = state
        self.set_starting_prices()
        self.show_warriors()
        self.is_buying = False
        self.number_buying = 1
        self.item_price = 0

    def exit(self):
        self.state.exit_bazaar()

    def set_starting_prices(self):
        """Set the starting prices for bazaar items"""
        self.food_price = 1
        self.warrior_price = self.gc.roll_dice(3) + 5 # 5-8
        self.beast_price = self.gc.roll_dice(9) + 17 # 17-26
        self.scout_price = self.gc.roll_dice(9) + 17 # 17-26
        self.healer_price = self.gc.roll_dice(9) + 17 # 17-26

    def on_button_click(self, text):
        """Handle button clicks"""
        self.gc.set_gm_status("")
        if text == "NO":
            if self.is_buying:
                # no, I dont need any more, buy please
                self.confirm_purchase()
            else:
                self.next_item()
        if text == "YES":
            if not self.is_buying:
                self.is_buying = True
                self.start_transaction()
            else:
                # yes, i'd like another please
                self.increase_number_buying()
        if text == "HAGGLE":
            self.gc.set_message("Player Haggled")

    def next_item(self):
        """Cycle to the next item in the bazaar"""
        if self.showing_warriors:
            self.show_food()
        elif self.showing_food:
            self.show_beast()
        elif self.showing_beast:
            self.show_scout()
        elif self.showing_scout:
            self.show_healer()
        elif self.showing_healer:
            self.show_warriors()

    def clear_flags(self):
        self.showing_warriors = False
        self.showing_food = False
        self.showing_beast = False
        self.showing_scout = False
        self.showing_healer = False

    def show_warriors(self):
        """Display the number of warriors the player has"""
        self.clear_flags()
        self.showing_warriors = True
        self.item_price = self.warrior_price
        self.display.set_value(self.warrior_price)
        self.gc.set_message(f"Warriors")
    
    def show_food(self):
        """Display the amount of food the player has"""
        self.clear_flags()
        self.showing_food = True
        self.item_price = self.food_price
        self.display.set_value(self.food_price)
        self.gc.set_message(f"Food")
    
    def show_beast(self):
        """Display if the player has a beast"""
        self.clear_flags()
        self.showing_beast = True
        self.item_price = self.beast_price
        self.display.set_value(self.beast_price)
        self.gc.set_message(f"Beast")
    
    def show_scout(self):
        """Display if the player has a scout"""
        self.clear_flags()
        self.showing_scout = True
        self.item_price = self.scout_price
        self.display.set_value(self.scout_price)
        self.gc.set_message(f"Scout")
    
    def show_healer(self):
        """Display if the player has a healer"""
        self.clear_flags()
        self.showing_healer = True
        self.item_price = self.healer_price
        self.display.set_value(self.healer_price)
        self.gc.set_message(f"Healer")
    
    def start_transaction(self):
        """Start a transaction for buying an item"""
        self.display.set_value(self.number_buying)

    def confirm_purchase(self):
        """Confirm the purchase of the selected items"""
        total_cost = self.number_buying * self.item_price

        if total_cost > self.player.gold:
            self.bazaar_closed()
            return
        
        self.player.gold -= total_cost
        self.gc.update_stats_display()
        self.gc.set_message(f"Purchased {self.number_buying} item(s) for {total_cost} gold.")
        self.exit()

    def bazaar_closed(self):
        """Handle the bazaar being closed"""
        self.gc.set_message("The bazaar is closed.")
        self.exit()

    def increase_number_buying(self):
        """Increase the number of items the player wants to buy"""
        self.number_buying += 1
        total_cost = self.number_buying * self.item_price

        if total_cost > self.player.gold:
            self.bazaar_closed()
       
        self.display.set_value(self.number_buying)
"""
Player Turn State

This state represents a single player's turn in the game.

"""

from typing import TYPE_CHECKING
from states.base_state import State
from player import Player

if TYPE_CHECKING:
    from game import GameController


class PlayerTurnState(State):

    def __init__(self, game_controller: "GameController"):
        super().__init__(game_controller)
        self.game_controller: "GameController" = game_controller
        self.display = self.game_controller.display
        
    def enter(self, player_number, **kwargs):
        self.is_turn_over = False
        self.player_number = player_number
        self.player: Player = self.game_controller.players[self.player_number - 1]
        self.display.set_value(self.player_number)
        self.next_player_number = self.player_number + 1 if self.player_number < len(self.game_controller.players) else 1
    
    def exit(self):
        pass

    def on_button_click(self, text):
        """Handle button clicks"""
        if text == "NO":
            if self.is_turn_over:
                self.end_turn()
        if text == "MOVE":
            if not self.is_turn_over:
                self.move()
                self.set_turn_over()
        if text == "TOMB":
            if not self.is_turn_over:
                self.tomb_ruin()
                self.set_turn_over()

    def set_turn_over(self):
        self.display.set_value(["minus", self.player_number])
        self.is_turn_over = True
        self.game_controller.clear_message()
        self.player.consume_food()
        self.game_controller.update_stats_display()

    def end_turn(self):
        """End the current player's turn and switch to the next player"""
        self.game_controller.state_machine.change_state("player_turn", player_number=self.next_player_number)

    # MOVE RESULTS
    # RESULT   HEX   DEC   LINE
    # ======   ===  =====  ====
    # LOST     0-2  00-02  2099
    # DRAGON   3-4  03-04  2142
    # PLAGUE   5-7  05-07  2280
    # BATTLE   8-A  08-10  2511
    # NOTHING  B-F  11-15   NA
    
    def move(self):
        """Handle the player's move action"""
        # Implement the logic for moving the player
        print(f"Player {self.player_number} is moving...")
        result = self.game_controller.roll_dice()

        print(f"Player {self.player_number} rolled a {result}")

        forced_move = self.game_controller.check_forced_moves()
        if forced_move is not None:
            result = forced_move

        if result <= 2:
            print(f"Player {self.player_number} got lost!")
            self.game_controller.set_message(f"Player {self.player_number} got lost!")
            self.player.get_lost()
        elif result <= 4:
            print(f"Player {self.player_number} encountered a dragon!")
            self.game_controller.set_message(f"Player {self.player_number} encountered a dragon!")
            self.player.dragon_attack()
        elif result <= 7:
            print(f"Player {self.player_number} encountered a plague!")
            self.game_controller.set_message(f"Player {self.player_number} encountered a plague!")
            self.player.get_plagued()
        elif result <= 10:
            print(f"Player {self.player_number} encountered a battle!")
            self.game_controller.set_message(f"Player {self.player_number} encountered a battle!")
        else:
            print(f"Player {self.player_number} encountered nothing!")
            self.game_controller.set_message(f"Player {self.player_number} encountered nothing!")

    # RESULT    HEX   DEC   LINE
    # ========  ===  =====  ====
    # CLOSE     0-1  00-01  3182
    # BATTLE    2-9  02-09  3189
    # TREASURE  A-F  10-16   NA

    def tomb_ruin(self):
        """Handle the player's tomb/ruin action"""
        print(f"Player {self.player_number} is exploring a tomb/ruin...")
        result = self.game_controller.roll_dice()

        print(f"Player {self.player_number} rolled a {result}")

        if result <= 1:
            print(f"Player {self.player_number} found a close encounter!")
            self.game_controller.set_message(f"Player {self.player_number} found a close encounter!")
        elif result <= 9:
            print(f"Player {self.player_number} encountered a battle!")
            self.game_controller.set_message(f"Player {self.player_number} encountered a battle!")
        else:
            print(f"Player {self.player_number} found treasure!")
            self.game_controller.set_message(f"Player {self.player_number} found treasure!")


    # RESULT     HEX   DEC   LINE
    # =======    ===  =====  ====
    # KEY*       0-9  00-09  3218
    # PEGASUS     A     10   3298
    # SWORD*      B     11   3321
    # WIZARD**    C     12   3343
    # GOLD ONLY  D-F  13-15   NA  

    def award_treasure(self):
        """Award treasure to the player"""
        print(f"Player {self.player_number} is being awarded treasure...")

        result = self.game_controller.roll_dice()
        result /= 2
        result += 13

        self.player.gold += result
        self.player.display("gold")

        self.game_controller.set_message(f"Player {self.player_number} has been awarded treasure!")

        result = self.game_controller.roll_dice()

        if result <= 9:
            print(f"Player {self.player_number} found a key!")
            self.game_controller.set_message(f"Player {self.player_number} found a key!")
            self.player.add_key()
        elif result == 10:
            print(f"Player {self.player_number} found Pegasus!")
            self.game_controller.set_message(f"Player {self.player_number} found Pegasus!")
            self.player.add_pegasus()
        elif result == 11:
            print(f"Player {self.player_number} found the Dragon Sword!")
            self.game_controller.set_message(f"Player {self.player_number} found the Dragon Sword!")
            self.player.add_dragon_sword()
        elif result == 12:
            print(f"Player {self.player_number} found the Wizard!")
            self.game_controller.set_message(f"Player {self.player_number} found the Wizard!")
            self.player.add_wizard()
        elif result <= 15:
            print(f"Player {self.player_number} only found gold!")


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

    def __init__(self, gc: "GameController"):
        super().__init__(gc)
        self.gc: "GameController" = gc
        self.display = self.gc.display
        
    def enter(self, player_number, **kwargs):
        """Set up the player turn UI"""
        self.gc.set_gm_status(f"Player {player_number} Turn. Waiting for action...")
        self.is_turn_over = False
        self.player_number = player_number
        self.player: Player = self.gc.players[self.player_number - 1]
        self.display.set_value(self.player_number)
        self.next_player_number = self.player_number + 1 if self.player_number < len(self.gc.players) else 1

    def exit(self):
        pass

    def on_button_click(self, text):
        """Handle button clicks"""
        self.gc.set_gm_status("")
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
        self.gc.clear_message()
        self.player.consume_food()
        self.gc.update_stats_display()
        self.gc.set_gm_status(f"Player {self.player_number} Turn Over. Press NO to end turn.")

    def end_turn(self):
        """End the current player's turn and switch to the next player"""
        self.gc.state_machine.change_state("player_turn", player_number=self.next_player_number)

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
        result = self.gc.roll_dice()

        print(f"Player {self.player_number} rolled a {result}")

        forced_move = self.gc.check_forced_moves()
        if forced_move is not None:
            result = forced_move

        if result <= 2:
            print(f"Player {self.player_number} got lost!")
            self.gc.set_message(f"Player {self.player_number} got lost!")
            self.player.get_lost()
        elif result <= 4:
            print(f"Player {self.player_number} encountered a dragon!")
            self.gc.set_message(f"Player {self.player_number} encountered a dragon!")
            self.player.dragon_attack()
        elif result <= 7:
            print(f"Player {self.player_number} encountered a plague!")
            self.gc.set_message(f"Player {self.player_number} encountered a plague!")
            self.player.get_plagued()
        elif result <= 10:
            print(f"Player {self.player_number} encountered a battle!")
            self.gc.set_message(f"Player {self.player_number} encountered a battle!")
        else:
            print(f"Player {self.player_number} encountered nothing!")
            self.gc.set_message(f"Player {self.player_number} encountered nothing!")

    # RESULT    HEX   DEC   LINE
    # ========  ===  =====  ====
    # CLOSE     0-1  00-01  3182
    # BATTLE    2-9  02-09  3189
    # TREASURE  A-F  10-16   NA

    def tomb_ruin(self):
        """Handle the player's tomb/ruin action"""
        print(f"Player {self.player_number} is exploring a tomb/ruin...")
        result = self.gc.roll_dice()

        print(f"Player {self.player_number} rolled a {result}")

        if result <= 1:
            print(f"Player {self.player_number} found a close encounter!")
            self.gc.set_message(f"Player {self.player_number} found a close encounter!")
        elif result <= 9:
            print(f"Player {self.player_number} encountered a battle!")
            self.gc.set_message(f"Player {self.player_number} encountered a battle!")
            self.do_battle()
        else:
            print(f"Player {self.player_number} found treasure!")
            self.gc.set_message(f"Player {self.player_number} found treasure!")


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
        self.gc.set_gm_status(f"Awarding treasure to Player {self.player_number}...")

        result = self.gc.roll_dice()
        result /= 2
        result += 13

        self.player.gold += result
        self.player.display("gold")

        self.gc.set_message(f"Player {self.player_number} has been awarded treasure!")

        result = self.gc.roll_dice()

        if result <= 9:
            print(f"Player {self.player_number} found a key!")
            self.gc.set_message(f"Player {self.player_number} found a key!")
            self.player.add_key()
        elif result == 10:
            print(f"Player {self.player_number} found Pegasus!")
            self.gc.set_message(f"Player {self.player_number} found Pegasus!")
            self.player.add_pegasus()
        elif result == 11:
            print(f"Player {self.player_number} found the Dragon Sword!")
            self.gc.set_message(f"Player {self.player_number} found the Dragon Sword!")
            self.player.add_dragon_sword()
        elif result == 12:
            print(f"Player {self.player_number} found the Wizard!")
            self.gc.set_message(f"Player {self.player_number} found the Wizard!")
            self.player.add_wizard()
        elif result <= 15:
            print(f"Player {self.player_number} only found gold!")


    def do_battle(self):
        """Handle battle logic for the player"""
        print(f"Player {self.player_number} is engaging in battle...")
        self.gc.set_gm_status(f"Player {self.player_number} is engaging in battle...")
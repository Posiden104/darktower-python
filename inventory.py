
class PlayerInventory:

    def __init__(self):
        self.gold = 30
        self.warriors = 6
        self.food = 10
        self.bronze_key = False
        self.silver_key = False
        self.gold_key = False
        self.dragon_sword = False
        self.beast = False
        self.healer = False
        self.kingdom = 1

    def can_enter_frontier(self) -> bool:
        match self.kingdom:
            case 1:
                return self.bronze_key and not self.gold_key
            case 2:
                return self.silver_key
            case 3:
                return self.gold_key
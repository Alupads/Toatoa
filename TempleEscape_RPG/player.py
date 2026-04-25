# player.py
class Player:
    def __init__(self):
        self.max_hp = 100
        self.hp = 100
        self.sanity = 100
        self.inventory = []
        self.saved_survivor = False
        self.ran_from_truth = False

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0: self.hp = 0

    def lose_sanity(self, amount):
        self.sanity -= amount
        if self.sanity < 0: self.sanity = 0

    def add_item(self, item):
        if item not in self.inventory:
            self.inventory.append(item)

    def has_item(self, item):
        return item in self.inventory

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def is_dead(self):
        return self.hp <= 0 or self.sanity <= 0

    # --- NEW: SAVE / LOAD DATA ---
    def to_dict(self):
        """Converts player stats to a dictionary for saving."""
        return {
            "hp": self.hp,
            "sanity": self.sanity,
            "inventory": self.inventory,
            "saved_survivor": self.saved_survivor,
            "ran_from_truth": self.ran_from_truth
        }

    def load_dict(self, data):
        """Loads player stats from a dictionary."""
        self.hp = data.get("hp", 100)
        self.sanity = data.get("sanity", 100)
        self.inventory = data.get("inventory", [])
        self.saved_survivor = data.get("saved_survivor", False)
        self.ran_from_truth = data.get("ran_from_truth", False)
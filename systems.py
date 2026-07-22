from collections import Counter
from data import FISH, ITEMS, RECIPES, RODS


class Inventory:
    def __init__(self):
        self.fish = Counter()
        self.items = Counter({"basic_bait": 3})

    def add_fish(self, fish_id, amount=1): self.fish[fish_id] += amount
    def add_item(self, item_id, amount=1): self.items[item_id] += amount

    def fillet(self, fish_id):
        if self.fish[fish_id] <= 0: return False
        self.fish[fish_id] -= 1
        for item_id, amount in FISH[fish_id]["materials"].items(): self.add_item(item_id, amount)
        return True


class Aquarium:
    def __init__(self):
        self.fish = Counter()
        self.level = 1
        self.capacity = 4
        self.money_buffer = 0.0

    def add(self, fish_id, inventory):
        if sum(self.fish.values()) >= self.capacity or inventory.fish[fish_id] <= 0: return False
        inventory.fish[fish_id] -= 1
        self.fish[fish_id] += 1
        return True

    def update(self, dt):
        per_minute = sum(FISH[k]["aquarium_income"] * n for k, n in self.fish.items())
        self.money_buffer += per_minute * dt / 60
        earned = int(self.money_buffer)
        self.money_buffer -= earned
        return earned

    def upgrade(self, money):
        cost = self.level * 100
        if money < cost: return money, False
        self.level += 1; self.capacity += 4
        return money - cost, True


class Player:
    def __init__(self):
        self.money = 50
        self.inventory = Inventory()
        self.aquarium = Aquarium()
        self.collection = set()
        self.rods = {"old_rod"}
        self.equipped_rod = "old_rod"

    def sell_fish(self, fish_id):
        if self.inventory.fish[fish_id] <= 0: return False
        self.inventory.fish[fish_id] -= 1; self.money += FISH[fish_id]["price"]
        return True

    def buy(self, item_id):
        price = ITEMS[item_id]["price"]
        if self.money < price: return False
        self.money -= price; self.inventory.add_item(item_id)
        return True

    def craft(self, recipe_id):
        recipe = RECIPES[recipe_id]
        if any(self.inventory.items[k] < n for k, n in recipe["cost"].items()): return False
        for k, n in recipe["cost"].items(): self.inventory.items[k] -= n
        if "rod" in recipe:
            self.rods.add(recipe["rod"]); self.equipped_rod = recipe["rod"]
        else:
            item_id, amount = recipe["makes"]; self.inventory.add_item(item_id, amount)
        return True

    @property
    def rod(self): return RODS[self.equipped_rod]

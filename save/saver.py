import json
import time
from collections import Counter
from pathlib import Path


class SaveManager:
    def __init__(self, path="save/save_code.json"):
        self.path = Path(path)

    def save(self, player):
        data = {
            "schema_version": 1,
            "saved_at": int(time.time()),
            "money": player.money,
            "fish": dict(player.inventory.fish),
            "items": dict(player.inventory.items),
            "collection": sorted(player.collection),
            "rods": sorted(player.rods),
            "equipped_rod": player.equipped_rod,
            "aquarium": {"fish": dict(player.aquarium.fish), "level": player.aquarium.level,
                         "capacity": player.aquarium.capacity},
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def load(self, player):
        if not self.path.exists(): return 0
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if "money" not in data: return 0  # 예전 개발용 저장 형식
            player.money = data["money"]
            player.inventory.fish = Counter(data.get("fish", {}))
            player.inventory.items = Counter(data.get("items", {}))
            player.collection = set(data.get("collection", []))
            player.rods = set(data.get("rods", ["old_rod"]))
            player.equipped_rod = data.get("equipped_rod", "old_rod")
            aq = data.get("aquarium", {})
            player.aquarium.fish = Counter(aq.get("fish", {})); player.aquarium.level = aq.get("level", 1)
            player.aquarium.capacity = aq.get("capacity", 4)
            return max(0, int(time.time()) - data.get("saved_at", int(time.time())))
        except (OSError, ValueError, KeyError, TypeError):
            return 0

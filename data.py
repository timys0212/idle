"""게임의 도감이자 모든 정적 데이터의 원본."""

RARITY_COLOR = {
    "일반": (210, 210, 190),
    "고급": (117, 201, 120),
    "희귀": (91, 155, 213),
    "영웅": (183, 120, 220),
}

FISH = {
    "pond_carp": {
        "name": "연못 붕어", "rarity": "일반", "price": 12,
        "weight": 55, "pattern": "steady", "aquarium_income": 0.2,
        "materials": {"fish_meat": 1},
        "description": "마을 연못에서 흔히 만나는 얌전한 붕어.",
    },
    "red_fish": {
        "name": "붉은 송어", "rarity": "고급", "price": 35,
        "weight": 28, "pattern": "dash", "aquarium_income": 0.7,
        "materials": {"fish_meat": 2, "red_scale": 1},
        "description": "짧고 강하게 도망치는 습성이 있다.",
    },
    "moon_koi": {
        "name": "달빛 비단잉어", "rarity": "희귀", "price": 140,
        "weight": 13, "pattern": "wave", "aquarium_income": 3.0,
        "materials": {"fish_meat": 2, "moon_scale": 1},
        "description": "달빛을 머금은 비늘이 물결처럼 빛난다.",
    },
    "storm_catfish": {
        "name": "폭풍 메기", "rarity": "영웅", "price": 520,
        "weight": 4, "pattern": "storm", "aquarium_income": 9.0,
        "materials": {"fish_meat": 4, "storm_whisker": 1},
        "description": "줄의 장력을 마구 흔드는 사나운 거대 메기.",
    },
}

ITEMS = {
    "fish_meat": {"name": "생선살", "price": 3, "description": "요리와 떡밥의 기본 재료."},
    "red_scale": {"name": "붉은 비늘", "price": 12, "description": "튼튼하고 따뜻한 비늘."},
    "moon_scale": {"name": "달빛 비늘", "price": 55, "description": "밤에 은은하게 빛난다."},
    "storm_whisker": {"name": "폭풍 수염", "price": 180, "description": "미세한 전기가 흐른다."},
    "basic_bait": {"name": "기본 떡밥", "price": 5, "description": "입질 시간을 조금 줄여준다."},
}

RODS = {
    "old_rod": {"name": "낡은 낚싯대", "max_wait": 25.0, "hook_bonus": 0.0, "escape_reduce": 0.0},
    "red_rod": {"name": "붉은 낚싯대", "max_wait": 20.0, "hook_bonus": 0.08, "escape_reduce": 0.03},
    "moon_rod": {"name": "월광 낚싯대", "max_wait": 15.0, "hook_bonus": 0.16, "escape_reduce": 0.07},
}

RECIPES = {
    "basic_bait": {"name": "기본 떡밥 x3", "makes": ("basic_bait", 3), "cost": {"fish_meat": 2}},
    "red_rod": {"name": "붉은 낚싯대", "rod": "red_rod", "cost": {"red_scale": 3, "fish_meat": 8}},
    "moon_rod": {"name": "월광 낚싯대", "rod": "moon_rod", "cost": {"moon_scale": 3, "red_scale": 5}},
}

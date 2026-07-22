from enum import Enum, auto
from math import sin
from random import choices, random, uniform
from data import FISH


class FishingState(Enum):
    IDLE = auto(); WAITING = auto(); BITING = auto(); REELING = auto()
    CAUGHT = auto(); ESCAPED = auto(); CANCELLED = auto()


class FishingSys:
    """낚시 한 사이클만 담당한다. 배낭과 돈은 Game이 처리한다."""
    HOOK_ESCAPE = {"perfect": 0.0, "good": 0.05, "nice": 0.09, "fail!": 0.60}

    def __init__(self):
        self.state = FishingState.IDLE
        self.elapsed = 0.0
        self.bite_at = 0.0
        self.fish_id = None
        self.hook_result = None
        self.progress = 0.0
        self.tension = 0.5
        self.retry_fish = None
        self.message = "SPACE로 낚시 시작"

    def start(self, rod, use_bait=False):
        if self.state not in (FishingState.IDLE, FishingState.CAUGHT, FishingState.ESCAPED, FishingState.CANCELLED): return False
        max_wait = rod["max_wait"] * (0.82 if use_bait else 1.0)
        self.elapsed = 0.0; self.bite_at = uniform(max(2.5, max_wait * 0.18), max_wait)
        self.fish_id = None; self.hook_result = None; self.progress = 0.0; self.tension = 0.5
        self.state = FishingState.WAITING; self.message = "대기 중...  (C: 취소)"
        return True

    def cancel(self):
        if self.state in (FishingState.WAITING, FishingState.BITING, FishingState.REELING):
            self.state = FishingState.CANCELLED; self.message = "찌를 다시 끌어올렸다."
            self.fish_id = None; return True
        return False

    def hook(self, rod):
        if self.state != FishingState.BITING: return False
        # 입질 직후 0.22초 부근이 완벽 판정이다. 좋은 장비일수록 판정 폭이 넓어진다.
        error = abs(self.elapsed - 0.22)
        bonus = rod["hook_bonus"]
        if error <= 0.12 + bonus: result = "perfect"
        elif error <= 0.32 + bonus: result = "good"
        elif error <= 0.72 + bonus: result = "nice"
        else: result = "fail!"
        self.hook_result = result; self.state = FishingState.REELING; self.elapsed = 0.0
        self.message = f"찌 물림  (걸림: {result})"
        return True

    def update(self, dt, rod, reeling=False):
        self.elapsed += dt
        if self.state == FishingState.WAITING and self.elapsed >= self.bite_at:
            if self.retry_fish and random() < 0.8:
                self.fish_id = self.retry_fish
                self.retry_fish = None
            else:
                self.fish_id = choices(list(FISH), weights=[FISH[k]["weight"] for k in FISH], k=1)[0]
            self.state = FishingState.BITING; self.elapsed = 0.0; self.message = "찌 물림!  SPACE로 후킹!"
        elif self.state == FishingState.BITING and self.elapsed >= 1.15 + rod["hook_bonus"]:
            self.retry_fish = self.fish_id
            self.hook_result = "fail!"; self.state = FishingState.REELING; self.elapsed = 0.0
            self.message = "Hooking mistake!  놓친 물고기 재등장 확률 80%"
        elif self.state == FishingState.REELING:
            self._reel(dt, rod, reeling)

    def _reel(self, dt, rod, reeling):
        fish = FISH[self.fish_id]
        speed = {"steady": 0.10, "dash": 0.13, "wave": 0.16, "storm": 0.22}[fish["pattern"]]
        disturbance = sin(self.elapsed * (4 + speed * 20)) * speed
        if fish["pattern"] == "storm": disturbance += sin(self.elapsed * 11) * 0.12
        self.tension += disturbance * dt + ((0.48 if reeling else -0.34) * dt)
        self.tension = max(0.0, min(1.0, self.tension))
        # 줄을 감되 장력이 안전 구간에 있을 때 가장 빨리 끌려온다.
        if reeling: self.progress += dt * (0.24 if 0.22 < self.tension < 0.82 else 0.06)
        escape = max(0.0, self.HOOK_ESCAPE[self.hook_result] - rod["escape_reduce"])
        if self.tension >= 0.995 or (escape and random() < escape * dt):
            self.state = FishingState.ESCAPED; self.message = "물고기가 줄을 놓았다!"
        elif self.progress >= 1.0:
            self.progress = 1.0; self.state = FishingState.CAUGHT
            self.retry_fish = None
            self.message = f"{fish['name']}을(를) 낚았다!"

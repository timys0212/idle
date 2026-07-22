from math import cos, pi, sin
import pygame
from data import FISH, ITEMS, RARITY_COLOR, RECIPES
from fishing import FishingState, FishingSys
from systems import Player


class Game:
    TABS = ["낚시", "도감", "배낭", "어항", "상점", "제작소"]

    def __init__(self):
        self.player = Player(); self.fishing = FishingSys(); self.tab = 0; self.cursor = 0
        self.font = None; self.small = None; self.notice = "1~6: 탭 이동"

    def attach_screen(self, screen):
        self.screen = screen
        if self.font is None:
            pygame.font.init()
            path = "C:/Windows/Fonts/malgun.ttf"
            try: self.font = pygame.font.Font(path, 24); self.small = pygame.font.Font(path, 18)
            except FileNotFoundError: self.font = pygame.font.Font(None, 28); self.small = pygame.font.Font(None, 21)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN: return
        if pygame.K_1 <= event.key <= pygame.K_6:
            self.tab = event.key - pygame.K_1; self.cursor = 0; return
        if event.key == pygame.K_UP: self.cursor = max(0, self.cursor - 1)
        if event.key == pygame.K_DOWN: self.cursor += 1
        if self.tab == 0:
            if event.key == pygame.K_c: self.fishing.cancel()
            elif event.key == pygame.K_SPACE:
                if self.fishing.state == FishingState.BITING: self.fishing.hook(self.player.rod)
                elif self.fishing.state != FishingState.REELING:
                    use_bait = self.player.inventory.items["basic_bait"] > 0
                    if use_bait: self.player.inventory.items["basic_bait"] -= 1
                    self.fishing.start(self.player.rod, use_bait)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE): self._tab_action()
        elif self.tab == 3 and event.key == pygame.K_u:
            self.player.money, ok = self.player.aquarium.upgrade(self.player.money)
            self.notice = "어항 확장 완료" if ok else "어항 확장 비용이 부족하다."

    def _tab_action(self):
        fish_ids = list(FISH); item_ids = list(ITEMS); recipe_ids = list(RECIPES)
        if self.tab == 2 and fish_ids:
            fish_id = fish_ids[self.cursor % len(fish_ids)]
            if pygame.key.get_mods() & pygame.KMOD_SHIFT: ok = self.player.inventory.fillet(fish_id); word = "손질"
            else: ok = self.player.sell_fish(fish_id); word = "판매"
            self.notice = f"{FISH[fish_id]['name']} {word} {'완료' if ok else '실패'}"
        elif self.tab == 3:
            fish_id = fish_ids[self.cursor % len(fish_ids)]
            self.notice = "어항에 보관했다." if self.player.aquarium.add(fish_id, self.player.inventory) else "어항이 가득 찼거나 물고기가 없다."
        elif self.tab == 4:
            item_id = item_ids[self.cursor % len(item_ids)]
            self.notice = "구매 완료" if self.player.buy(item_id) else "돈이 부족하다."
        elif self.tab == 5:
            recipe_id = recipe_ids[self.cursor % len(recipe_ids)]
            self.notice = "제작 완료" if self.player.craft(recipe_id) else "재료가 부족하다."

    def update(self, dt):
        holding = pygame.key.get_pressed()[pygame.K_SPACE]
        before = self.fishing.state
        self.fishing.update(dt, self.player.rod, holding)
        if before != FishingState.CAUGHT and self.fishing.state == FishingState.CAUGHT:
            self.player.inventory.add_fish(self.fishing.fish_id); self.player.collection.add(self.fishing.fish_id)
        self.player.money += self.player.aquarium.update(dt)

    def draw(self, surface):
        surface.fill((24, 29, 38)); w, h = surface.get_size()
        pygame.draw.rect(surface, (46, 56, 70), (0, 0, w, 58))
        for i, name in enumerate(self.TABS):
            color = (255, 220, 120) if i == self.tab else (205, 215, 220)
            self._text(surface, f"{i+1}.{name}", (22 + i * 135, 17), color, self.small)
        self._text(surface, f"{self.player.money} G   장비: {self.player.rod['name']}", (w - 370, 17), (255, 225, 130), self.small)
        [self._draw_fishing, self._draw_collection, self._draw_inventory, self._draw_aquarium, self._draw_shop, self._draw_crafting][self.tab](surface)
        self._text(surface, self.notice, (25, h - 36), (180, 190, 205), self.small)

    def _draw_fishing(self, s):
        w, h = s.get_size(); pygame.draw.rect(s, (79, 145, 169), (0, 330, w, h - 330))
        pygame.draw.circle(s, (245, 190, 100), (130, 220), 58); pygame.draw.polygon(s, (70, 55, 48), [(80,190),(180,190),(155,145),(105,145)])
        self._text(s, "낚시하는 고양이", (45, 85), (240, 230, 190), self.font)
        self._text(s, self.fishing.message, (340, 150), (255, 225, 95), self.font)
        if self.fishing.state == FishingState.BITING:
            self._draw_hooking_circle(s)
        elif self.fishing.state == FishingState.REELING:
            self._bar(s, (340, 220, 500, 26), self.fishing.progress, (100, 210, 135), "포획")
            self._bar(s, (340, 275, 500, 26), self.fishing.tension, (230, 105, 85), "장력")
            self._text(s, "SPACE를 누르며 장력을 22~82%로 유지", (340, 315), (235,235,220), self.small)
        else: self._text(s, "SPACE: 시작/후킹   C: 낚시 취소", (340, 220), (230,235,220), self.small)

    def _draw_hooking_circle(self, surface):
        fishing = self.fishing
        center = (650, 355)
        radius = 125

        if fishing.circle_draw_progress < 1.0:
            # 입질 순간 화면 틀이 잠깐 밝아지고 원주가 0.5초 동안 생성된다.
            pulse = 1.0 - fishing.circle_draw_progress
            glow = int(110 * pulse)
            pygame.draw.rect(surface, (145 + glow, 180 + glow // 2, 205), surface.get_rect(), 8)
            self._ring_segment(surface, center, radius, 0.0,
                               fishing.circle_draw_progress, (255, 235, 145), 7)
            return

        # 완성된 원 위에 50%를 기준으로 대칭인 판정 구간을 표시한다.
        pygame.draw.circle(surface, (85, 96, 110), center, radius, 5)
        self._ring_segment(surface, center, radius, 0.40, 0.44, (80, 155, 225), 10)
        self._ring_segment(surface, center, radius, 0.44, 0.47, (100, 205, 125), 10)
        self._ring_segment(surface, center, radius, 0.47, 0.53, (255, 220, 90), 12)
        self._ring_segment(surface, center, radius, 0.53, 0.56, (100, 205, 125), 10)
        self._ring_segment(surface, center, radius, 0.56, 0.60, (80, 155, 225), 10)

        progress = fishing.hook_progress
        angle = -pi / 2 + 2 * pi * progress
        inner = (center[0] + cos(angle) * (radius - 18), center[1] + sin(angle) * (radius - 18))
        outer = (center[0] + cos(angle) * (radius + 18), center[1] + sin(angle) * (radius + 18))
        pygame.draw.line(surface, (255, 255, 255), inner, outer, 8)
        pygame.draw.circle(surface, (255, 220, 105), (int(outer[0]), int(outer[1])), 5)

        difference = progress - 0.5
        if abs(difference) <= 0.03:
            live_text, color = "PERFECT", (255, 225, 90)
        elif difference < 0:
            live_text, color = "FAST", (105, 190, 245)
        else:
            live_text, color = "LATE", (245, 135, 105)
        self._center_text(surface, live_text, center, color)
        percent = self.small.render(f"{progress * 100:04.1f}%", True, (225, 230, 235))
        surface.blit(percent, percent.get_rect(center=(center[0], center[1] + 34)))
        self._text(surface, "50%에 맞춰 SPACE", (555, 510), (240, 235, 215), self.small)

    @staticmethod
    def _ring_segment(surface, center, radius, start, end, color, width):
        steps = max(2, int((end - start) * 100))
        points = []
        for i in range(steps + 1):
            progress = start + (end - start) * i / steps
            angle = -pi / 2 + 2 * pi * progress
            points.append((center[0] + cos(angle) * radius,
                           center[1] + sin(angle) * radius))
        pygame.draw.lines(surface, color, False, points, width)

    def _center_text(self, surface, text, center, color):
        rendered = self.font.render(text, True, color)
        surface.blit(rendered, rendered.get_rect(center=center))

    def _draw_collection(self, s):
        self._title(s, "모든 생물과 물건의 기록"); y=125
        for k, f in FISH.items():
            known = k in self.player.collection; name = f["name"] if known else "???"
            self._text(s, f"[{f['rarity']}] {name}  -  {f['description'] if known else '아직 발견하지 못했다.'}", (55,y), RARITY_COLOR[f["rarity"]], self.small); y+=42

    def _draw_inventory(self, s):
        self._title(s, "배낭  (Enter: 판매 / Shift+Enter: 손질)"); y=125
        for i,(k,f) in enumerate(FISH.items()): self._row(s,i,y,f"{f['name']} x{self.player.inventory.fish[k]}   판매 {f['price']}G"); y+=36
        y+=20
        for k,item in ITEMS.items(): self._text(s,f"{item['name']} x{self.player.inventory.items[k]}",(620,y),(195,205,190),self.small); y+=30

    def _draw_aquarium(self, s):
        aq=self.player.aquarium; self._title(s,f"어항 Lv.{aq.level}  {sum(aq.fish.values())}/{aq.capacity}  (Enter: 보관 / U: {aq.level*100}G 확장)"); y=125
        for i,(k,f) in enumerate(FISH.items()): self._row(s,i,y,f"{f['name']}  배낭:{self.player.inventory.fish[k]} / 어항:{aq.fish[k]}  분당 {f['aquarium_income']}G"); y+=38

    def _draw_shop(self, s):
        self._title(s,"상점  (Enter: 구매)"); y=125
        for i,(k,item) in enumerate(ITEMS.items()): self._row(s,i,y,f"{item['name']}  {item['price']}G - {item['description']}"); y+=42

    def _draw_crafting(self, s):
        self._title(s,"제작소  (Enter: 제작)"); y=125
        for i,(k,r) in enumerate(RECIPES.items()):
            cost=", ".join(f"{ITEMS[x]['name']} {n}" for x,n in r["cost"].items()); self._row(s,i,y,f"{r['name']}  필요: {cost}"); y+=46

    def _title(self,s,text): self._text(s,text,(45,82),(255,220,135),self.font)
    def _row(self,s,i,y,text): self._text(s,("▶ " if i==self.cursor else "  ")+text,(55,y),(245,230,180) if i==self.cursor else (205,210,205),self.small)
    def _text(self,s,text,pos,color,font): s.blit(font.render(str(text),True,color),pos)
    def _bar(self,s,rect,value,color,label):
        pygame.draw.rect(s,(45,48,55),rect); pygame.draw.rect(s,color,(rect[0],rect[1],int(rect[2]*value),rect[3])); self._text(s,f"{label} {int(value*100)}%",(rect[0]+8,rect[1]+3),(255,255,255),self.small)

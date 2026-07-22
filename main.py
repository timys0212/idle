import pygame
from display import Screen
from game import Game
from save.saver import SaveManager


class Main:
    def __init__(self):
        pygame.init(); self.window = Screen(); self.game = Game(); self.game.attach_screen(self.window); self.running = True
        self.saver = SaveManager()
        away_seconds = self.saver.load(self.game.player)
        if away_seconds:
            earned = int(sum(__import__("data").FISH[k]["aquarium_income"] * n for k, n in self.game.player.aquarium.fish.items()) * away_seconds / 60)
            self.game.player.money += earned
            self.game.notice = f"쉬는 동안 어항에서 {earned}G를 벌었다."

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                else: self.game.handle_event(event)
            self.game.update(self.window.dt); self.game.draw(self.window.surface); self.window.update()
        self.saver.save(self.game.player); pygame.quit()


if __name__ == "__main__": Main().run()

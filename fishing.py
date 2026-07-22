from util import Timer as timer, Signal as signal
from random import randint

class FishingSys:
  def __init__(self):
    # fishing stick setting
    self.max_fishing_time = 1.0 # 낚싯대랑 연동해서 정해짐 (기본값 1초)
    self.hooking_state = ["perfect", "good", "nice", "fail!"]
    self.states = ["<Fishing>", "<fishing float Bited>", f"hooking : {self.hooking_state}"]

    self.stack = 0

  def start(self):
    timer("fishing_waiting").start()

    self.state : str = self.states[0]

  def run(self):
    # 확률적으로 물고기가 입질하게 되고 self.delay_time의 시간이 걸리면 확정적으로 입질
    # 놓치면 다음에 나올 확률 증가.
    if not len(self.state) > 0:
      return "fishing_waiting isn't started"

    if self.state == self.states[0]:
      if not timer("fishing_waiting").trigger(self.max_fishing_time):
        self.stack += 1
        if timer("fishing_waiting").trigger(1*self.stack):
          val = randint(0, 100)
          if val <= 10: # 10%
            self.states[1]
            self.stack = 0
            timer("fishing_waiting").stop()

      else:
        self.state
        self.stack = 0
        timer("fishing_waiting").stop()

    elif self.state == self.states[1]:
      timer("fishing_scene").start()

      if timer("fishing_scene").trigger(8):
        self.state = ""
        


    elif self.state == self.states[2]:
      pass


# ========================================================================================= test code


if __name__ == "__main__":
  import pygame

  from display import Screen
  from game import Game

  FS = FishingSys()

  class Main:
    def __init__(self):
      self.window = Screen()
      self.game = Game()
      self.running = True
      timer.init(self.window)

    def run(self):
      FS.start()
      while self.running:
        # key event
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            self.running = False
            self.window.close()

          if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
              self.running = False
              self.window.close()

        FS.run()

        # //
        self.window.surface.fill("white")

        timer("bited").update()
        timer("hooking").update()

        self.window.update()

  main = Main()
  main.run()
import pygame

from display import Screen

class Main:
  def __init__(self):
    self.window = Screen()
    self.running = True

  def run(self):
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

      # calculate


      # //
      self.window.surface.fill("white")

      # draw


      self.window.update()

if __name__ == "__main__":
  main = Main()
  main.run()
import pygame
from typing import NoReturn, TypeAlias, Callable, Optional

ExitValue: TypeAlias = int | str | None
ExitCode: TypeAlias = ExitValue | Callable[[], ExitValue]

class Screen:
  _ExitCode: TypeAlias = ExitCode

  def __init__(self, width: int = 1250, fps: int = 60):
    self.x = width
    self.y = int(width * (9 / 16))
    self.fps = fps

    self.surface = pygame.display.set_mode((self.x, self.y))
    self.caption = "main_game"
    pygame.display.set_caption(self.caption)

    self.clock = pygame.time.Clock()

  def fill(self, r: int, g: int, b: int):
    return self.surface.fill((r, g, b))

  def update(self):
    pygame.display.update()
    self.clock.tick(self.fps)

  def close(self, code: _ExitCode = None) -> NoReturn:
    # code가 함수면 실행해서 값으로 바꿈 ( return값으로 )
    if callable(code):
      code = code()

    if pygame.get_init(): # 중복 종료 방어
      pygame.quit()

    raise SystemExit(0 if code is None else code)

from display import Screen as Window

class Game:
  def __init__(self):
    self.screen : Window

  def get_value_from_main(self, screen_info : Window):
    self.screen = screen_info

  def run(self):
    pass
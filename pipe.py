from random import randint

class Pipe:
  def __init__(self, height, width):
    self.x = width
    self.space = randint((height - 100) // 10 * 2, (height - 100) // 10 * 8)
  
  def move_and_draw(self, screen, up, down):
    self.x -= 3
    self.up_pipe = up.get_rect(topleft=(self.x, (self.space - 100 - 490)))
    self.down_pipe = down.get_rect(topleft=(self.x, self.space + 100))
    screen.blit(up, self.up_pipe.topleft)
    screen.blit(down, self.down_pipe.topleft)
    
  def check_collision(self, player):
    if player.colliderect(self.up_pipe) or player.colliderect(self.down_pipe):
      return True
    return False
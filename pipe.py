from random import randint

class Pipe:
  def __init__(self):
    self.x = 800
    self.space = randint(1430 // 10 * 2, 1430 // 10 * 8)
  
  def move_and_draw(self, screen, up, down):
    self.x -= 10
    self.up_pipe = up.get_rect(topleft=(self.x, (self.space - 210 - 980)))
    self.down_pipe = down.get_rect(topleft=(self.x, self.space + 210))
    screen.blit(up, self.up_pipe.topleft)
    screen.blit(down, self.down_pipe.topleft)
    
  def check_collision(self, player):
    if player.colliderect(self.up_pipe) or player.colliderect(self.down_pipe):
      return True
    return False
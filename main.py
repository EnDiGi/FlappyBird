import pygame as pg
import sys
from bird import Bird
from pipe import Pipe
from base import Base

pg.init()

# Variables and constants
WIDTH, HEIGHT = 715, 1530
FPS = 60
clock = pg.time.Clock()

WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Flappy Bird")
BG = pg.transform.scale(pg.image.load("background.jpg"), (WIDTH, HEIGHT))
PLAYER = pg.transform.scale(pg.image.load("bird.png"), (80, 57))
PIPE_DOWN = pg.transform.scale(pg.image.load("pipe.png"), (120, 980))
PIPE_UP = pg.transform.flip(PIPE_DOWN, False, True)
BASE = pg.transform.scale(pg.image.load("base.png"), (WIDTH, 100))

def draw(birdX, birdY, pipes, started, font, score):
  text = font.render(str(score), True, (255, 255, 255))
  rect = text.get_rect(center = (357, 150))
  
  WIN.blit(BG, (0, 0))
  WIN.blit(BASE, (0, 1430))
  WIN.blit(PLAYER, (birdX, birdY))
  WIN.blit(text, rect)
  
  if started:
    for pipe in pipes:
      pipe.move_and_draw(WIN, PIPE_UP, PIPE_DOWN)
    pipes = [pipe for pipe in pipes if pipe.x >= 120]
        
def check_loss(coord, pipes, base):
  bird_rect = pg.Rect(coord[0], coord[1], PLAYER.get_width(), PLAYER.get_height())
  if base.check_collision(coord):
    return True
  for pipe in pipes:
    if pipe.check_collision(bird_rect):
      return True
  return False
 
def increase_score(coord, pipes, score):
  bird_rect = pg.Rect(coord[0], coord[1], PLAYER.get_width(), PLAYER.get_height())
  if any(pipe.x == bird_rect.x for pipe in pipes):
    score += 1
  return score

def main():
  WIN.fill((0, 0, 0))
  font = pg.font.Font(None, 250)
  
  while True:
    score = game(font)
    end(score, font)
    
def end(score, font):
  clock = pg.time.Clock()
  new = False
  
  small_font = pg.font.Font(None, 74)
  
  with open("best.txt", "r") as f:
    old = int(f.read())
    
  best = max(old, score)
  if best == score:
    new = True
  if old == best:
    new = False
    
  with open("best.txt", "w") as f:
    f.write(str(best))
      
  while True:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        sys.exit()
      elif event.type in [pg.FINGERDOWN, pg.KEYDOWN]:
        return
    
    score_txt = font.render(str(score), True, (255, 255, 255))
    rect = score_txt.get_rect(center = (WIDTH // 2, HEIGHT // 2))
    
    if new:
      best_txt = small_font.render("New highscore!" , False, (255, 255, 255))
      best_rect = best_txt.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 100))
    else:
      best_txt = small_font.render(f"Best: {best}" , False, (255, 255, 255))
      best_rect = best_txt.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 100))
      
    WIN.blit(score_txt, rect)
    WIN.blit(best_txt, best_rect)
    
    pg.display.update()
    clock.tick(FPS)

def game(font):
  running = True
  
  birdX, birdY = 50, 700
  started = False
  pipes = []
  frames = 0
  score = 0
    
  j_frame = 0 # Current jump frame
  j_frames = 10 # Jump frames
  
  bird = Bird()
  base = Base()
  
  while running:
    velY = 0
    if started:
      velY += bird.fall()
      
      if frames % 50 == 0:
        pipes.append(Pipe())
        frames = 0
      
    if j_frame == j_frames:
      j_frame = 0
      clock.tick(FPS)
      continue
      
    if j_frame: # If we're jumping
      j_frame += 1
      velY = (bird.flap() // j_frames)
       
    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        sys.exit()
      elif event.type in [pg.FINGERDOWN, pg.KEYDOWN]:
        if j_frame: # If it's already jumping
          j_frame = 0
        j_frame += 1
        velY += (bird.flap() // j_frames)
        started = True
    
    birdY += velY # Applies the speed changes made previously   
    if birdY <= 0:
      birdY = 0 # Prevents the user from flying to the top of the screen
    score = increase_score([birdX, birdY], pipes, score)
    draw(birdX, birdY, pipes, started, font, score)
    pg.display.flip()
    if check_loss([birdX, birdY], pipes, base):
      return score
    frames += 1
    clock.tick(FPS)

if __name__ == '__main__':
  main()
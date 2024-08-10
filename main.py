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

def draw(birdX, birdY, pipes, started):
  WIN.blit(BG, (0, 0))
  WIN.blit(BASE, (0, 1430))
  WIN.blit(PLAYER, (birdX, birdY))
  if started:
    for pipe in pipes:
      pipe.move_and_draw(WIN, PIPE_UP, PIPE_DOWN)
      if pipe.x <= -100:
        pipes.remove(pipe)

def check_loss(coord, pipes, base):
  bird_rect = pg.Rect(coord[0], coord[1], PLAYER.get_width(), PLAYER.get_height())
  if base.check_collision(coord):
    return True
  for pipe in pipes:
    if pipe.check_collision(bird_rect):
      return True
  return False
  
def main():
  running = True
  
  birdX, birdY = 50, 700
  started = False
  pipes = []
  frames = 0
  WIN.fill((0, 0, 0))
  
  j_frame = 0 # Current jump frame
  j_frames = 10 # Jump frames
  
  bird = Bird()
  base = Base()
  
  while running:
    if check_loss([birdX, birdY], pipes, base):
      break
    velY = 0
    if started:
      velY += bird.fall()
      
      if frames % 40 == 0:
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
        running = False
        pg.quit()
        sys.exit()
      elif event.type in [pg.FINGERDOWN, pg.KEYDOWN]:
        if j_frame: # If it's already jumping
          j_frame = 0
        j_frame += 1
        velY += (bird.flap() // j_frames)
        started = True
    
    birdY += velY # Applies the speed changes made previously
    draw(birdX, birdY, pipes, started)       
    pg.display.flip()
    frames += 1
    clock.tick(FPS)

if __name__ == '__main__':
  main()
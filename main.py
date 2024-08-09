import pygame as pg
import sys
from bird import Bird

# Variables and constants
WIDTH, HEIGHT = 715, 1530
FPS = 60
clock = pg.time.Clock()

WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Flappy Bird")
BG = pg.transform.scale(pg.image.load("background.jpg"), (WIDTH, HEIGHT))
PLAYER = pg.transform.scale(pg.image.load("bird.png"), (80, 57))

def draw(birdX, birdY):
  WIN.blit(BG, (0, 0))
  WIN.blit(PLAYER, (birdX, birdY))
  
def main():
  running = True
  
  birdX, birdY = 50, 700
  started = False
  
  j_frame = 0 # Current jump frame
  j_frames = 17 # Jump frames
  
  while running:
    bird = Bird()
    velY = 0
    if started:
      velY += bird.fall()
    
    if j_frame == j_frames:
      j_frame = 0
      clock.tick(FPS)
      continue
    if j_frame:
      j_frame += 1
      velY = (bird.flap() // j_frames)
       
    for event in pg.event.get():
      if event.type == pg.QUIT:
        running = False
        pg.quit()
        sys.exit()
      elif event.type in [pg.FINGERDOWN, pg.KEYDOWN]:
        if j_frame: # If it's already jumping
          continue
        j_frame += 1
        velY = (bird.flap() // j_frames)
        started = True
          
    birdY += velY # Applies the speed changes made previously
    draw(birdX, birdY)       
    pg.display.update()
    clock.tick(FPS)

if __name__ == '__main__':
  main()
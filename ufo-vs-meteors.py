import sys
import time
import pygame
from random import randint

pygame.font.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((1024, 768))

class EndException(Exception): pass
class CrashException(Exception): pass

rocket_y = 384
down = up = False

enemies = [(1024, randint(5, 733))]

z = 0
v = 0

if len(sys.argv) < 2:
  a = 0.05
  p = 30
elif sys.argv[1] == 'hard':
  a = 0.1
  p = 25
elif sys.argv[1] == 'pro':
  a = 0.5
  p = 20
elif sys.argv[1] == 'normal':
  a = 0.05
  p = 30
elif sys.argv[1] == 'easy':
  a = 0.01
  p = 40
else:
  a = 0.05
  p = 30

start = time.time()

try:
  while True:
    clock.tick(30)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        raise EndException

      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          up = True
        elif event.key == pygame.K_DOWN:
          down = True

      elif event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
          up = False
        elif event.key == pygame.K_DOWN:
          down = False

    if up:
      rocket_y -= 8
    if down:
      rocket_y += 8

    if rocket_y < 15:
      rocket_y = 15
    elif rocket_y > 752:
      rocket_y = 752

    v += a
    z += v

    if randint(0, 50) > p:
      enemies += [(1024+z, randint(5, 733))]

    screen.fill((0, 0, 0))

    # draw rocket
    pygame.draw.circle(screen, (25, 55, 255), (100, rocket_y), 15, 10)

    # draw enemies
    for (x, y) in enemies:
      pygame.draw.line(screen, (200, 0, 0), (x-z, y),
                       (x-z, y+v*1.2), int(v) + 1)

    pygame.display.flip()

    for i in range(rocket_y-15, rocket_y+16):
      if screen.get_at((100, i)) == (200, 0, 0, 255):
        raise CrashException

except EndException:
  pass

except CrashException:
  t = time.time() - start

  font = pygame.font.Font(pygame.font.get_default_font(), 30)
  text = font.render('Crash!!! time: ' + str(t) + 's', True, (255, 150, 20))

  screen.blit(text, (0, 0))
  pygame.display.flip()

  time.sleep(3)

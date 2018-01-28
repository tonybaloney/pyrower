import pygame
import serial
import itertools
import statistics
from collections import deque

pygame.font.init()
myfont = pygame.font.SysFont('Arial', 30)

gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('PyRower')
bg = pygame.image.load("images/water.png")

clock = pygame.time.Clock()
speeds = deque([0,0,0,0], 100)

crashed = False
textsurface = None
speed = 0.
distance = 0.

ser = serial.Serial('/dev/cu.usbmodem1421')  # open serial port
print(ser.name)         # check which port was really used

while not crashed:
    speed += 1

    gameDisplay.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    value = ser.readline().decode('ascii')     # write a string
    
    speed, distance = value.split(',')
    speed = float(speed.strip())
    distance = float(distance.strip())

    speeds.append(speed)
    speed_av = statistics.mean(list(itertools.islice(speeds, len(speeds)-4, len(speeds))))

    speed_text = myfont.render('Speed : {}'.format(speed_av), False, (0, 0, 0))
    distance_text = myfont.render('Distance : {}m'.format(distance), False, (0, 0, 0))

    gameDisplay.blit(speed_text,(10,10))
    gameDisplay.blit(distance_text,(10,40))

    pygame.display.update()
    clock.tick(10)
ser.close()             # close port

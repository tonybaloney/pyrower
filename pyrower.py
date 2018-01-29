import pygame
import serial
import itertools
import statistics
from collections import deque
import argparse
from enum import Enum
from interface import ArduinoInterface, FileInterface

parser = argparse.ArgumentParser()
parser.add_argument('--test', )

# TODO : Calibration option
MIN_SPEED = 0
SLOW_SPEED = 10
FASTEST_SPEED = 150


class RowerStatus(Enum):
    pull = 1
    drag = 2


rower_images = { 
    RowerStatus.drag: pygame.image.load("images/drag.png"),
    RowerStatus.pull: pygame.image.load("images/pull.png")
}


def main(args):
    pygame.font.init()
    myfont = pygame.font.SysFont('Arial', 30)

    gameDisplay = pygame.display.set_mode((800,600))
    pygame.display.set_caption('PyRower')
    bg = pygame.image.load("images/water.png")

    clock = pygame.time.Clock()
    speeds = deque([0,0,0,0], 100)

    crashed = False
    speed = 0.
    distance = 0.
    last_speed_av = 0.

    if args.test:
        interface = FileInterface('test_out.txt')
    else:
        interface = ArduinoInterface('/dev/cu.usbmodem1421')

    interface.connect()

    while not crashed:
        gameDisplay.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        # Read the total distance travelled and the speed from the device
        value = interface.readline().decode('ascii')     # write a string
        
        speed, distance = value.split(',')
        speed = float(speed.strip())
        distance = float(distance.strip())

        # Speed average is a scrolling mean based on the last 4 measurements
        speeds.append(speed)
        speed_av = statistics.mean(list(itertools.islice(speeds, len(speeds)-4, len(speeds))))
        
        # If faster than last time, assume rower is pulling
        rower_status = RowerStatus.drag if speed_av < last_speed_av else RowerStatus.pull

        # Record this speed average
        last_speed_av = speed_av

        # Draw the stats on screen
        speed_text = myfont.render('Speed : {}'.format(speed_av), False, (0, 0, 0))
        distance_text = myfont.render('Distance : {}m'.format(distance), False, (0, 0, 0))

        gameDisplay.blit(speed_text,(10,10))
        gameDisplay.blit(distance_text,(10,40))

        gameDisplay.blit(
            rower_images[rower_status],
            (100, 200 + (FASTEST_SPEED - speed_av)))

        pygame.display.update()
        clock.tick(10)
    interface.close()             # close port

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
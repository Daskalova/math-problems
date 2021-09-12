import pygame
from pygame.locals import *

import numpy as np
import math
import sys

pygame.init()

WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont('arial', 10, bold=True)

x_space = 10
y_space = 12
columns = int(WIDTH / x_space)
rows = int(HEIGHT / y_space)

x_offset = WIDTH / 2
y_offset = HEIGHT / 2


R1 = 40 # raadius 2D circle
R2 = 100 # radius torus
A, B = 0, 0
K2 = 5000
K1 = WIDTH * K2 * 3/(8*(R1 + R2))

illumination_values = ['.', ',', '-', '~', ':', ';', '=', '!', '*', '#', '$', '@']


def draw(x, y, char):
    text = font.render(char, True, (255,255,255))
    screen.blit(text, (x,y))


while True:
    screen.fill(((0,0,0)))

    # store final output of characters
    output = []
    for i in range(rows):
        col = []
        for j in range(columns):
            col.append(" ")
        output.append(col)

    # store z-values
    zbuffer = []
    for i in range(rows):
        col = []
        for j in range(columns):
            col.append(0)
        zbuffer.append(col)

    cosA, sinA = math.cos(A), math.sin(A)
    cosB, sinB = math.cos(B), math.sin(B)

    # theta goes around the cross-sectional circle of a torus
    for theta in np.arange(0, 2*math.pi, 0.15):
        cosTheta, sinTheta = math.cos(theta), math.sin(theta)

        # phi goes around the axis of revolution of a torus
        for phi in np.arange(0, 2*math.pi, 0.10):
            cosPhi, sinPhi = math.cos(phi), math.sin(phi)

            # x and y coordinate of the circle, before revolving
            circleX = R2 + R1 * cosTheta
            circleY = R1 * sinTheta

            # 3D coordinate of a torus after rotations
            x = circleX * (cosB * cosPhi + sinA * sinB * sinPhi) - circleY * cosA * sinB
            y = circleX * (sinB * cosPhi - sinA * cosB * sinPhi) + circleY * cosA * cosB
            z = circleX * (cosA * sinPhi) + circleY * sinA + K2
            ooz = 1 / z

            # x and y projection on the 2D screen
            xp = math.floor(x * K1 * ooz)
            yp = math.floor(-y * K1 * ooz)

            # calculate luminance
            l = cosPhi * cosTheta * sinB - cosA * cosTheta * sinPhi \
                - sinA * sinTheta + cosB * (cosA * sinTheta - cosTheta * sinA * sinPhi) 

            if l > -0.8:
                l = abs(l)
                yc = int((yp + y_offset)/y_space)
                xc = int((xp + x_offset)/x_space)

                # check if point is closer towards viewer than previous stored point
                if ooz > zbuffer[yc][xc]:
                    zbuffer[yc][xc] = ooz
                    L = round(l*8)
                    output[yc][xc] = illumination_values[L]
    
    for a in range(rows):
        for b in range(columns):
            draw(b*x_space, a*y_space, output[a][b])

    # prevent A and B to go up to inifnity
    if A > 6.283 and A < 6.2831:
        A, B = 0, 0
    else:
        A += 0.06
        B += 0.04
        

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    pygame.display.update()

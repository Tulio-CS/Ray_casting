from pygame.locals import *
from operator import add, sub
import pygame
import sys
import math
import random

pygame.init()

#/////////////////////////////////////////////////////////////////////////////////
WINDOW_SIZE = (800, 600)     # Altura x Largura em pixels
NUM_RAYS = 360               # Entre 1 e 360 
SOLID_RAYS = False           # Estranho, melhores resultados com NUM_RAYS = 360
NUM_WALLS = 5                # The amount of randomly generated walls
DISPLAY_MODE = "showcase"    # "darkness" or "showcase" or ""
#/////////////////////////////////////////////////////////////////////////////////


screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(WINDOW_SIZE)

mx, my = pygame.mouse.get_pos()
lastClosestPoint = (0, 0)
running = True
rays = []
walls = []
particles = []


if DISPLAY_MODE == "darkness":
    display_color = (255, 255, 255)
    ray_color = "black"
    wall_color = "white"

elif DISPLAY_MODE == "showcase":
    display_color = (0, 0, 0)
    ray_color = "white"
    wall_color = "white"  

elif DISPLAY_MODE == "":
    display_color = (255, 255, 255)  #in RGB
    ray_color = "black"
    wall_color = "white"

class Ray:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.dir = (math.cos(angle), math.sin(angle))

    def update(self, mx, my):
        self.x = mx
        self.y = my

    def checkCollision(self, wall):
        x1 = wall.start_pos[0]
        y1 = wall.start_pos[1]
        x2 = wall.end_pos[0]
        y2 = wall.end_pos[1]

        x3 = self.x
        y3 = self.y
        x4 = self.x + self.dir[0]
        y4 = self.y + self.dir[1]
    
        # Using line-line intersection formula to get intersection point of ray and wall
        # Where (x1, y1), (x2, y2) are the ray pos and (x3, y3), (x4, y4) are the wall pos
        denominador = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        numerador = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        if denominador == 0:
            return None
        
        t = numerador / denominador
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominador

        if 1 > t > 0 and u > 0:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            collidePos = [x, y]
            return collidePos

class Wall:
    def __init__(self, start_pos, end_pos, color = wall_color):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.slope_x = end_pos[0] - start_pos[0]
        self.slope_y = end_pos[1] - start_pos[1]
        if self.slope_x == 0:
            self.slope = 0
        else:
            self.slope = self.slope_y / self.slope_x
        self.length = math.sqrt(self.slope_x**2 + self.slope_y**2)

    def draw(self):
        pygame.draw.line(display, self.color, self.start_pos, self.end_pos, 3)

for i in range(0, 360, int(360/NUM_RAYS)):
    rays.append(Ray(mx, my, math.radians(i)))

def drawRays(rays, walls, color = ray_color):
    global lastClosestPoint
    for ray in rays:
        closest = 100000
        closestPoint = None
        for wall in walls:
            intersectPoint = ray.checkCollision(wall)
            if intersectPoint is not None:
                # Get distance between ray source and intersect point
                ray_dx = ray.x - intersectPoint[0]
                ray_dy = ray.y - intersectPoint[1]
                # If the intersect point is closer than the previous closest intersect point, it becomes the closest intersect point
                distance = math.sqrt(ray_dx**2 + ray_dy**2)
                if (distance < closest):
                    closest = distance
                    closestPoint = intersectPoint

        if closestPoint is not None:
            pygame.draw.line(display, color, (ray.x, ray.y), closestPoint)
            if SOLID_RAYS:
                pygame.draw.polygon(display, color, [(mx, my), closestPoint, lastClosestPoint])
                lastClosestPoint = closestPoint

def generateWalls():
    walls.clear()

    walls.append(Wall((0, 0), (WINDOW_SIZE[0], 0)))
    walls.append(Wall((0, 0), (0, WINDOW_SIZE[1])))
    walls.append(Wall((WINDOW_SIZE[0], 0), (WINDOW_SIZE[0], WINDOW_SIZE[1])))
    walls.append(Wall((0, WINDOW_SIZE[1]), (WINDOW_SIZE[0], WINDOW_SIZE[1])))

    for i in range(NUM_WALLS):
        start_x = random.randint(0, WINDOW_SIZE[0])
        start_y = random.randint(0, WINDOW_SIZE[1])
        end_x = random.randint(0, WINDOW_SIZE[0])
        end_y = random.randint(0, WINDOW_SIZE[1])
        walls.append(Wall((start_x, start_y), (end_x, end_y)))

def draw():
    display.fill(display_color)

    for wall in walls:
        wall.draw()

    for particle in particles:
        particle.draw()

    drawRays([ray for ray in rays], [wall for wall in walls])

    screen.blit(display, (0, 0))

    pygame.display.update()


if len(walls) == 0:
    generateWalls()

while running:
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            pygame.quit()

        if event.type == KEYDOWN:
            # Re-randomize walls on Space
            if event.key == pygame.K_SPACE:
               generateWalls()

    for ray in rays:
        ray.update(mx, my)

    draw()



import math
import time
import random
import pygame

WIDTH, HEIGHT = 1280, 736
TILESIZE = 32

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gameg")

global objects
objects = []

class Object():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def update(self):
        pass
    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

class Player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_force = 0
        self.y_force = 0
        self.jump_count = 0 
        self.max_jumps = 1
        self.isColiding = False
        self.onWall = False
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.y_force = 0
        self.jump_count = 0
        self.rect.x = self.x
        self.rect.y = self.y
        self.isColiding = False
        self.onWall = False
    def check_collision(self):
        self.isColiding = False
        self.onWall = False
        for obj in objects:
            if self.rect.colliderect(obj.rect) == True:
                dx = self.rect.centerx - obj.rect.centerx
                dy = self.rect.centery - obj.rect.centery
                if abs(dx) > abs(dy):
                    if dx > 0:
                        self.x = obj.rect.right + 4
                        self.jump_count = 0
                        self.onWall = True
                    else:
                        self.x = obj.rect.left - self.rect.width - 4
                        self.jump_count = 0
                        self.onWall = True
                else:
                    if dy > 0:
                        self.y = obj.rect.bottom
                        if self.y_force < 0:
                            self.y_force = 0
                    else:
                        self.y_force = 0
                        self.jump_count = 0
                        self.y = obj.rect.top - self.rect.height
                self.isColiding = True
        if self.isColiding == False:
            self.jump_count = 1
    def update(self):
        self.x += self.x_force
        self.y += self.y_force
        self.y_force += 0.003
        self.rect.x = self.x
        self.rect.y = self.y
        self.check_collision()
        if self.y_force > 1:
            self.y_force = 1
        keys = pygame.key.get_pressed()
        if self.jump_count < self.max_jumps:
            if keys[pygame.K_w] and self.onWall == False:
                self.y_force = -1
                self.jump_count += 1
        if keys[pygame.K_d] and self.onWall == False:
            self.x_force = 0.25
        elif keys[pygame.K_a] and self.onWall == False:
            self.x_force = -0.25
        else:
            self.x_force = 0
        if self.onWall == True:
            self.y_force += 0.03
    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

class Map():
    global tilemap
    tilemap = []
    def new_map(map):
        objects.clear()
        tilemap = map
        for y, row in enumerate(tilemap):
            for x, column in enumerate(row):
                if column == 'B':
                    objects.append(Object(x * TILESIZE, y * TILESIZE))
                if column == 'P':
                    global player
                    player = None
                    player = Player(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
                    player.reset(x * TILESIZE, y * TILESIZE)
    def delete_map():
        tilemap.clear()
        objects.clear()

class Main():
    def __init__(self):
        Map.new_map( [
        'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
        'B...B..................................B',
        'B...B..................................B',
        'B...B..................................B',
        'B...B..................................B',
        'B...B................BBBBB.............B',
        'B...B....................B.............B',
        'B...BBBBBBBBB............B.............B',
        'B...B..................................B',
        'B.P.B..................................B',
        'B...B..................................B',
        'B...B..................................B',
        'B...B........BBBBBBBBBB................B',
        'B...B..................................B',
        'B...B.....................BBBBBBBBBBBBBB',
        'B.....................BB...............B',
        'B......................................B',
        'B..........BBBBBBBBBB..................B',
        'B.......B..............................B',
        'B......BB..............................B',
        'B.....BBB..............................B',
        'B....BBBB..............................B',
        'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    ])
    def update(self):
        player.update()
        for obj in objects:
            obj.update()
    def draw(self):
        player.draw()
        for obj in objects:
            obj.draw()
    def main(self):
        run = True
        while run:
            #update
            self.update()
            #draw
            pygame.display.flip()
            screen.fill((0, 0, 0))
            self.draw()
            #events
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
        pygame.quit()

main_instance = Main()
main_instance.main()
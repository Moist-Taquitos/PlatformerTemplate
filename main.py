import time
import random
import pygame
from pygame import mixer
import turtle
import os
from colours import *
from tkinter import *
from tkinter import messagebox
# TODO: Movement and gravity, Player 1, moveset for character "Mr.Hitbox", test dummy, moveset for character "Stock", player 2, blocking, combo system, teching,

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 1200
HEIGHT = 1000
TITLE = "Platformer Template (Has gravity and stuff)"


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([100, 150])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.change_y = 0
        self.change_x = 0
        self.rect.x, self.rect.y = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        # Keeping player in the screen
        # Top and bottom
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        # Left and right
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        self.calc_grav()

        self.rect.y += self.change_y #remember to actually use self.change_y instead of just setting it

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 0.5
        else:
            self.change_y += 0.34

        # See if we are on the ground.
        if self.rect.y >= HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = HEIGHT - self.rect.height


class Mr_Hitbox_Punch(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.tick = 0
        self.image = pygame.Surface([50, 50])
        self.image.fill(RED1)
        self.rect = self.image.get_rect()
        self.player = player


    def update(self):
        print (self.rect.x, self.rect.y)
        self.tick += 1
        if self.tick == 10:
            self.kill()
            self.tick = 0
        self.rect.x, self.rect.y = (self.player.rect.right+50, self.player.rect.y+50)

        print(self.tick)

class Mr_Hitbox_Kick(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.tick = 0
        self.image = pygame.Surface([100, 50])
        self.image.fill (RED1)
        self.rect = self.image.get_rect()
        self.player = player

    def update(self):
        self.tick += 1
        if self.tick == 15:
            self.kill()
            self.tick = 0
            self.rect.x, self.rect.y = (self.player.rect.x+50, self.player.rect.y+50)

        print(self.tick)


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # Sprite groups
    all_sprites_group = pygame.sprite.Group()
    mr_hitbox_punch_sprites_group = pygame.sprite.Group()
    mr_hitbox_kick_sprites_group = pygame.sprite.Group()

    player = Player()
    mr_hitbox_punch = Mr_Hitbox_Punch(player)
    mr_hitbox_kick = Mr_Hitbox_Kick(player)
    all_sprites_group.add(player)
    all_sprites_group.add(mr_hitbox_punch)
    all_sprites_group.add(mr_hitbox_kick)

    # ----- LOCAL VARIABLES
    done = False
    direction = 0
    crouch = False
    jump = 0
    time_since_last_jump = 0

    time_since_last_kick = 0
    clock = pygame.time.Clock()

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pressed = pygame.key.get_pressed()
        # ----- LOGIC
        if player.rect.y >= HEIGHT - player.rect.height and player.change_y >= 0:
            player.change_y = 0
            player.rect.y = HEIGHT - player.rect.height
            jump = 0
        if pressed[pygame.K_w]:
            if time_since_last_jump >= 0.5*60:
                if jump < 2:
                    player.change_y = -10
                    #player.rect.y -= player.change_y  # moves the player upward
                    direction = 1
                    jump += 1
                    time_since_last_jump = 0
        if pressed[pygame.K_s]:
            player.change_y = 10
            player.rect.y += player.change_y
            direction = 2
            crouch = True
        else: crouch = False
        if pressed[pygame.K_a]:
            player.change_x = 5
            player.rect.x -= player.change_x
            direction = 3
        if pressed[pygame.K_d]:
            player.change_x = 5
            player.rect.x += player.change_x
            direction = 4
        if pressed[pygame.K_LSHIFT] and pressed[pygame.K_d]:
            player.change_x = 10
            player.rect.x += player.change_x
        if pressed[pygame.K_LSHIFT] and pressed[pygame.K_a]:
            player.change_x = 10
            player.rect.x -= player.change_x
        if pressed[pygame.K_q]:
            all_sprites_group.add(mr_hitbox_punch)
        if pressed[pygame.K_e]:
                all_sprites_group.add(mr_hitbox_kick)

        all_sprites_group.update()

        # ----- RENDER
        screen.fill(WHITE)
        all_sprites_group.draw(screen)



        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(60)
        time_since_last_jump += 1
        print(time_since_last_jump)

    pygame.quit()


if __name__ == "__main__":
    main()

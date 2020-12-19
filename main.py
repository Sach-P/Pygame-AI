"""
Author: Sachin Patel (github: Sach-P)
December 18, 2020

AI learns, using NEAT, to play a game I made using pygame.
Try changing some of the values in the config text file or the values the players are rewarded to see different results.
"""
import pygame
import os
import neat
import math
import random

from pygame.locals import (
    QUIT,
)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
gen = 0

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((0, 170, 255))
        self.rect = self.surf.get_rect(center = (x, y))
        self.distFromGoal = math.sqrt(((goal.rect.centery-self.rect.centery)*(goal.rect.centery-self.rect.centery)) + ((goal.rect.centerx-self.rect.centerx)*(goal.rect.centerx-self.rect.centerx)))
        self.preDistFromGoal = self.distFromGoal

    def update(self, move):
        if move == 1:
            self.rect.move_ip(0, -4)
        if move == 2:
            self.rect.move_ip(0, 4)
        if move == 3:
            self.rect.move_ip(-4, 0)
        if move == 4:
            self.rect.move_ip(4, 0)

        # Boundaries
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        self.distFromGoal = math.sqrt(((goal.rect.centery-self.rect.centery)*(goal.rect.centery-self.rect.centery)) + ((goal.rect.centerx-self.rect.centerx)*(goal.rect.centerx-self.rect.centerx)))
    
    def setPreDist(self):
        self.preDistFromGoal = self.distFromGoal

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Wall, self).__init__()
        self.surf = pygame.Surface((50, (SCREEN_HEIGHT*2-50)))
        self.surf.fill((200, 90, 130))
        self.rect = self.surf.get_rect(center = (x, y))

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Goal, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect(center = (x, y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, velX, velY, rVal):
        super(Enemy, self).__init__()
        self.x = x
        self.y = y
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((rVal, 0, 0))
        self.rect = self.surf.get_rect(center = (x, y))
        self.speedX = velX
        self.speedY = velY

    def update(self):

      if self.rect.left <= 0:
          self.speedX = abs(self.speedX)
      elif self.rect.right >= SCREEN_WIDTH:
          self.speedX = -self.speedX

      if self.rect.top <= 0:
          self.speedY = abs(self.speedY)
      elif self.rect.bottom >= SCREEN_HEIGHT:
          self.speedY = -self.speedY

      self.rect.move_ip(self.speedX, self.speedY)

    def respawn(self):
        self.rect = self.surf.get_rect(center = (self.x, self.y))


pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

all_sprites = pygame.sprite.Group() # Sprite Groups

# Walls
wall1 = Wall(0, 0)
wall2 = Wall(SCREEN_WIDTH, 500)

walls = pygame.sprite.Group()

walls.add(wall1)
all_sprites.add(wall1)
walls.add(wall2)
all_sprites.add(wall2)

# Goal
goal = Goal(SCREEN_WIDTH-13, 12)
all_sprites.add(goal)

# Enemies
enemies = pygame.sprite.Group()

enemy1 = Enemy(SCREEN_WIDTH-20, SCREEN_HEIGHT/2+75, 10, 0, 255)
enemy2 = Enemy(SCREEN_WIDTH-20, 50, 10, 0, 255)
enemy3 = Enemy(20, SCREEN_HEIGHT/2-75, 10, 0, 255)
enemy4 = Enemy(20, SCREEN_HEIGHT-50, 10, 0, 255)

enemy5 = Enemy(50, 20, 0, 10, 255)
enemy6 = Enemy(SCREEN_WIDTH/2+75, 20, 0, 10, 255)
enemy7 = Enemy(SCREEN_WIDTH/2-75, SCREEN_HEIGHT-20, 0, 10, 255)
enemy8 = Enemy(SCREEN_WIDTH-50, SCREEN_HEIGHT-20, 0, 10, 255)

enemy9 = Enemy(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 0, 10, 255)
enemy10 = Enemy(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 10, 0, 255)
enemy11 = Enemy(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 0, -10, 255)
enemy12 = Enemy(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, -10, 0, 255)

enemy13 = Enemy(12, 0, 0, -5, 155)
enemy14 = Enemy(SCREEN_WIDTH-20, SCREEN_HEIGHT-12, 5, 0, 100)
enemy15 = Enemy(12, 12, 5, 0, 100)

enemies.add(enemy1)
all_sprites.add(enemy1)
enemies.add(enemy2)
all_sprites.add(enemy2)
enemies.add(enemy3)
all_sprites.add(enemy3)
enemies.add(enemy4)
all_sprites.add(enemy4)

enemies.add(enemy5)
all_sprites.add(enemy5)
enemies.add(enemy6)
all_sprites.add(enemy6)
enemies.add(enemy7)
all_sprites.add(enemy7)
enemies.add(enemy8)
all_sprites.add(enemy8)

enemies.add(enemy9)
all_sprites.add(enemy9)
enemies.add(enemy10)
all_sprites.add(enemy10)
enemies.add(enemy11)
all_sprites.add(enemy11)
enemies.add(enemy12)
all_sprites.add(enemy12)

enemies.add(enemy13)
all_sprites.add(enemy13)
enemies.add(enemy14)
all_sprites.add(enemy14)
enemies.add(enemy15)
all_sprites.add(enemy15)

# Display Text
def text_objects(text, font, c):
    textSurface = font.render(text, True, c)
    return textSurface, textSurface.get_rect()

def message_display(text, size, x, y, color):
    largeText = pygame.font.Font("freesansbold.ttf", size)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = (x, y)
    screen.blit(TextSurf, TextRect)

def main(genomes, config):

    global gen
    gen += 1

    # Intialize NEAT
    players = []
    nets = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        players.append(Player(10, SCREEN_HEIGHT))
        ge.append(genome)
    
    distFromGoal = 0
    preDistFromGoal = 0
    
    for player in players:
        all_sprites.add(player)

    running = True
    hud_display = True

    clock = pygame.time.Clock()
  
    for enemy in enemies:
        enemy.respawn()
    
    # Main loop
    while running and len(players) > 0:
        # Frame-rate | Lower for visualization, Higher for quicker results
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()

        enemies.update()
        walls.update()

        screen.fill((0, 0, 0))

        remainingPlayers = len(players)

        if hud_display:
            message_display("Gen: " + str(gen), 90, SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 'grey')
            message_display("Players Alive: " + str(remainingPlayers), 50, SCREEN_WIDTH/2, SCREEN_HEIGHT/2+75, 'grey')
        
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
         

        for x, player in enumerate(players):
            
            output = nets[players.index(player)].activate((player.rect.centery, player.rect.centerx, distFromGoal, preDistFromGoal)) 
       
            if output[0] > 0.5:
                player.update(1)
            if output[1] > 0.5:
                player.update(2)
            if output[2] > 0.5:
                player.update(3)
            if output[3] > 0.5:
                player.update(4)

            # Reward if the player gets closer to the goal
            if player.distFromGoal < player.preDistFromGoal:
                ge[x].fitness += 10/((player.distFromGoal/100)+1)   
            elif player.distFromGoal == player.preDistFromGoal:
                ge[x].fitness -= 1
                if not player.rect.center == goal.rect.center:
                    player.update(random.randint(1, 4))

            player.setPreDist()

            # Check enemy collision         
            if pygame.sprite.spritecollideany(player, enemies):
                ge[x].fitness -= 2
                nets.pop(players.index(player))
                ge.pop(players.index(player))
                players.pop(players.index(player))
                player.kill()
            
            # Check is player has reached the goal
            elif player.rect.center == goal.rect.center:
                message_display("WINNER", 115, SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 'white')
                message_display("Gen: " + str(gen), 35, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 75, 'white')
                ge[x].fitness += 25
                hud_display = False
                for enemy in enemies:
                    enemy.kill()

            # Check wall collision
            if wall1.rect.colliderect(player.rect):
                if player.rect.left <= wall1.rect.right:
                    player.rect.left = wall1.rect.right        
            elif wall2.rect.colliderect(player.rect):
                if player.rect.right >= wall2.rect.left:
                    player.rect.right = wall2.rect.left

        pygame.display.flip()


def run(config_file):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    p = neat.Population(config)

    # Statistical results
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 100)

# Configuration file
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
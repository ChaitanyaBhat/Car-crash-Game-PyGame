import pygame
from pygame.locals import * #(RLEACCEL,QUIT,KEYDOWN,KEYUP,K_ESCAPE,K_LEFT,K_RIGHT,K_UP,K_DOWN)
import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.surf = pygame.image.load("bluecar.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect( center = (
            0, (screenHeight/2 - 40)
        ))
    
    def update(self, pressed_keys):
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screenWidth:
            self.rect.right = screenWidth
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screenHeight:
            self.rect.bottom = screenHeight

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("redcar.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(
                random.randint(screenWidth + 10, screenWidth + 20),
                random.randint(0, screenHeight)
            ))
        self.speed = random.randint(1, 6)
    def update(self):
        self.rect.move_ip(-10, 0)
        if self.rect.right < 0:
            self.kill()

class Blocks(pygame.sprite.Sprite):
    def __init__(self):
        super(Blocks, self).__init__()
        self.surf = pygame.Surface((20, 5))
        self.surf.fill((255, 255, 255))
        self.rect1 = self.surf.get_rect(center = (-5, 100))
        self.rect2 = self.surf.get_rect(center = (-5, 300))
        self.rect3 = self.surf.get_rect(center = (-5, 500))
        self.speed = 10
    def update(self):
        self.rect1.move_ip(5, 0)
        if self.rect1.right < 0:
            self.kill()
        self.rect2.move_ip(5, 0)
        if self.rect2.right < 0:
            self.kill()
        self.rect3.move_ip(5, 0)
        if self.rect2.right < 0:
            self.kill()

pygame.init()

screenWidth = 1000
screenHeight = 600

screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption('Car Crash')
roadImg = pygame.image.load('cementroad2.jpeg')
clock = pygame.time.Clock()

ADDENEMY = pygame.USEREVENT+1
pygame.time.set_timer(ADDENEMY,1000)

ADDBLOCKS = pygame.USEREVENT + 5
pygame.time.set_timer(ADDBLOCKS, 500)

player = Player()
enemies = pygame.sprite.Group()
blocks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
while running:
    blocks.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:    
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDBLOCKS:
            new_block = Blocks()
            blocks.add(new_block)


    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    screen.fill((0,0,0))
    
   
    screen.blit(roadImg,(0,0))
    for entity in blocks:
        screen.blit(entity.surf, entity.rect1)
        screen.blit(entity.surf, entity.rect2)
        screen.blit(entity.surf, entity.rect3)

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
quit()


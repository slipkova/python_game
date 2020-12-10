import pygame
from random import *
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    score = 0
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("images/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                randint(SCREEN_WIDTH +20, SCREEN_WIDTH + 100),
                randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = randint(5, 15)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("images/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                randint(SCREEN_WIDTH +20, SCREEN_WIDTH + 100),
                randint(0, SCREEN_HEIGHT)
            )
        )


    def update(self):
        self.rect.move_ip(-3, 0)
        if self.rect.right < 0:
            self.kill()


class Cake(pygame.sprite.Sprite):
    def __init__(self):
        super(Cake, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("images/cake.png").convert(), [30, 25])
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                randint(SCREEN_WIDTH +20, SCREEN_WIDTH + 100),
                randint(0, SCREEN_HEIGHT)
            )
        )


    def update(self):
        self.rect.move_ip(-4, 0)
        if self.rect.right < 0:
            self.kill()
        elif pygame.sprite.collide_rect(player, self):
            self.kill()
            player.score += 1


pygame.mixer.init()
pygame.font.init()
pygame.init()

clock = pygame.time.Clock()
font = pygame.font.SysFont('', 50)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 300)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1200)
ADDCAKE = pygame.USEREVENT +3
pygame.time.set_timer(ADDCAKE, 1700)

player = Player()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
cakes = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

pygame.mixer.music.load("sound/Sky_dodge_theme.ogg")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.1)

up_sound = pygame.mixer.Sound("sound/Jet_up.ogg")
down_sound = pygame.mixer.Sound("sound/Jet_down.ogg")
boom_sound = pygame.mixer.Sound("sound/Boom.ogg")

up_sound.set_volume(0.1)
down_sound.set_volume(0.1)
boom_sound.set_volume(0.2)

running = True
while running:

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
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
        elif event.type == ADDCAKE:
            new_cake = Cake()
            cakes.add(new_cake)
            all_sprites.add(new_cake)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    enemies.update()
    clouds.update()
    cakes.update()

    screen.fill((135, 206, 250))


    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        up_sound.stop()
        down_sound.stop()
        pygame.mixer.music.stop()
        pygame.time.delay(50)
        boom_sound.play()
        pygame.time.delay(500)
        running = False

    screen.blit(font.render(f"SCORE: {player.score}", False, (0, 0, 0)), [SCREEN_WIDTH - 200, 5])
    pygame.display.flip()

    clock.tick(35)

pygame.mixer.quit()
pygame.quit()
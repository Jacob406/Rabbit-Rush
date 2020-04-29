import pygame
import random
import os
import time
import math
import webbrowser

WIDTH = 1100
HEIGHT = 700
FPS = 60 
speed = 15
score = 0
timer = 61

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
Light_blue = (0, 0, 200) 
YELLOW = (255, 255, 0)
ORANGE = (255,165,0)
BGCOLOR = (0, 155, 155)
change_c = BLACK

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rabbit Rush!")
clock = pygame.time.Clock()

file = open("scoring.txt", "w+")

font_name = pygame.font.match_font('comicsansms')
def draw_text(surf, text, size, x, y, colour):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "bunny1.png"))
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        self.speed = speed


    def update(self):
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT] and self.rect.x > 50:
            self.rect.x -= speed

        if keystate[pygame.K_RIGHT] and self.rect.x < 1125 - 70 - 5 - 50:
            self.rect.x += speed

        if keystate[pygame.K_UP] and self.rect.y > 61:
            self.rect.y -= speed

        if keystate[pygame.K_DOWN] and self.rect.y < 695 - 70 - 5:
            self.rect.y += speed

        if keystate[pygame.K_ESCAPE]:
            pygame.quit()
            quit()


class Egg(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "smallegg.png"))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, 750)
        self.rect.y = random.randint(140, 550)



all_sprites = pygame.sprite.Group()
all_mobs = pygame.sprite.Group()

player = Player()
egg = Egg()

all_sprites.add(player, egg)
all_mobs.add(egg)

def intro():
    pygame.display.update()
    pygame.mixer.music.load('TitleScreen.wav')
    pygame.mixer.music.play(-1)
    start = pygame.image.load(os.path.join(img_folder, "start1.png"))
    space_to_start = pygame.image.load(os.path.join(img_folder, "start_space.png"))
    start.get_rect()
    screen.blit(start, (195, 200))
    screen.blit(space_to_start, (335, 350))
    pygame.display.update()

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                pygame.mixer.music.stop()
                game_loop()
        pygame.display.update()




def game_loop():
    global change_c
    global score
    global timer
    pygame.mixer.music.load('game_music.mp3')
    pygame.mixer.music.play(-1)
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        

        grass = (pygame.image.load(os.path.join(img_folder, "grass1.jpg")))
        grass_large = pygame.transform.scale(grass, (WIDTH, HEIGHT))
        title = pygame.image.load(os.path.join(img_folder, "rabbitrush2.png"))
        trees = pygame.image.load(os.path.join(img_folder, "trees.png"))

        screen.blit(trees, (0, 0))
        screen.blit(grass_large, (0, 0))
        screen.blit(title, (395, 10))

        seconds = clock.tick() / 750.0
        timer -= seconds
        display_timer = math.trunc(timer)

        if display_timer <= 15:
            change_c = YELLOW

        if display_timer <= 10:
            change_c = ORANGE

        if display_timer >= 30:
            change_c = GREEN

        if display_timer <= 5:
            change_c = RED
            pygame.display.update()

        score_text = draw_text(screen, "Score: " + str(score), 50, 900, 0, BLACK)
        time_text = draw_text(screen, "Time left: " + str(display_timer), 50, 220, 0, change_c)
        all_sprites.update()

        hits = pygame.sprite.spritecollide(player, all_mobs, True)
        for mob_sprite in hits:
            score += 10
            global speed
            speed += 1
            m = Egg()
            all_sprites.add(m)
            all_mobs.add(m)
        all_sprites.draw(screen)
        
        if display_timer <= 0:
            pygame.mixer.music.fadeout(10000)
            screen.fill((WHITE))
            game_over = pygame.image.load(os.path.join(img_folder, "game_over1.png"))
            screen.blit(game_over, (545, 50))
            end = pygame.image.load(os.path.join(img_folder, "end_screen.jpg"))
            screen.blit(end, (0, 0))
            draw_text(screen, "Well done, your score was " + str(score) + "!", 30, 260, 575, BLACK)
            pause = pygame.image.load(os.path.join(img_folder, "press_space_quit.png"))
            s_media = pygame.image.load(os.path.join(img_folder, "websites.png"))
            s_media_text = pygame.image.load(os.path.join(img_folder, "social_media.png"))
            screen.blit(s_media, (700, 250))
            screen.blit(pause, (535, 145))
            screen.blit(s_media_text, (535, 400))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                pygame.display.update()
                file.write("Your Score Is: " + str(score))
                pygame.quit()
                quit()

            elif keys[pygame.K_t]:
                webbrowser.open("https://twitter.com")

            elif keys[pygame.K_f]:
                webbrowser.open("https://www.facebook.com")

            elif keys[pygame.K_i]:
                webbrowser.open("https://www.instagram.com") 

        pygame.display.update()


intro()
file.write("Your Score Is: " + str(score))
pygame.mixer.quit()
pygame.quit()
file.close()

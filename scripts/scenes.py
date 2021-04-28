import sys

import pygame

import model
import usefull_func


pygame.init()

clock = pygame.time.Clock()

WIDTH = 800
HEIGHT = 600

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Combat")

RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREY = (170, 170, 170)
BLACK = (0, 0, 0)

FPS = 60

class GameOver:
    def __init__(self):
        self.game_text = model.FontCustom("Game", 80, WHITE, (320, 200))
        self.over_text = model.FontCustom("Over", 80, WHITE, (320, 263))
        self.menu_button = model.Button("Menu", BLACK, GREY, (310, 400))
        self.square = pygame.Rect(150, 100, 500, 400)
        self.click = False

        self.game_over_run = True

    def input_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over_run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True

    def logic(self):
        mx, my = pygame.mouse.get_pos()
        if self.menu_button.rect.collidepoint(mx, my):
            if self.click:
                menu = MainMenu()
                menu.run()
                self.click = False

    def draw(self, window):
        pygame.draw.rect(window, BLACK, self.square)
        self.game_text.draw(window)
        self.over_text.draw(window)
        self.menu_button.draw(window)

    def run(self):
        while self.game_over_run:
            clock.tick(FPS)

            self.input_handle()

            self.logic()

            self.draw(WINDOW)
            
            pygame.display.update()


class MainMenu:
    def __init__(self):
        self.space_text = model.FontCustom("SPACE", 80, WHITE, (300, 200))
        self.combat_text = model.FontCustom("COMBAT", 80, WHITE, (285, 263))
        self.start_button = model.Button("Start", BLACK, GREY, (310, 400))
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.shader = False
        self.click = False

        self.menu_run = True

    def input_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main_run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True

    def effect(self):
        if self.shader and (self.rect.width != 920 and self.rect.height != 920):
            self.rect.width += 20
            self.rect.height += 20
        elif not self.shader and (self.rect.width != -20 and self.rect.height != -20):
            self.rect.width -= 20
            self.rect.height -= 20

    def logic(self):
        mx, my = pygame.mouse.get_pos()
        if self.start_button.rect.collidepoint((mx, my)):
            if self.click:
                game = Game()
                game.run()
                self.click = False
            
            self.shader = True
        else:
            self.shader = False

        self.effect()

    def draw(self, window):
        WINDOW.fill((0, 0, 0))
        pygame.draw.rect(window, GREY, self.rect)
        self.space_text.draw(window)
        self.combat_text.draw(window)
        self.start_button.draw(WINDOW)

    def run(self):
        while self.menu_run:
            clock.tick(FPS)

            self.input_handle()

            self.logic()
                    
            self.draw(WINDOW)

            pygame.display.update()


class Game:
    def __init__(self):
        self.background = usefull_func.load_image("desert-backgorund.png", 800, 600, 0)

        self.player_one = model.Player("sprite_02.png", 16, 25, (400, 500), 0)
        self.player_two = model.Player("sprite_02.png", 16, 25, (400, 90), 180)
        self.players = pygame.sprite.Group((self.player_one, self.player_two))

        self.player_one_hb = model.Bar("bar_0.png", RED, self.player_one.health, 10, (690, 580))
        self.player_two_hb = model.Bar("bar_0.png", RED, self.player_two.health, 10, (10, 10))

        self.player_one_bullets = []
        self.player_two_bullets = []

        self.game_run = True

    def input_handle(self):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.game_run = False
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    self.game_run = False
                    
                elif event.key == pygame.K_RCTRL:
                    self.player_one_bullets.append(model.Bullet("laser_1.png", 16, 16, self.player_one.position, self.player_one.direction))
                    
                elif event.key == pygame.K_LCTRL:
                    self.player_two_bullets.append(model.Bullet("laser_1.png", 16, 16, self.player_two.position, self.player_two.direction))

                player_one_keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
                # the first index is K_s because the second player faces upside down
                player_two_keys = [pygame.K_s, pygame.K_w, pygame.K_a, pygame.K_d]

                self.player_one.keydown_movement(event, player_one_keys)
                self.player_two.keydown_movement(event, player_two_keys)
                
            elif event.type == pygame.KEYUP:
                player_one_keys_turn = [pygame.K_LEFT, pygame.K_RIGHT]
                player_two_keys_turn = [pygame.K_a, pygame.K_d]
                
                self.player_one.keyup_movement(event, player_one_keys_turn)
                self.player_two.keyup_movement(event, player_two_keys_turn)

    def logic(self):
        for bullet in self.player_one_bullets:
            bullet.move(True)

            if usefull_func.is_collide(bullet, self.player_two):
                self.player_two.health -= 1
                bullet.delete(self.player_one_bullets)

            if bullet.position.x < 0 or bullet.position.x > WIDTH or bullet.position.y < 0 or bullet.position.y > HEIGHT:
                bullet.delete(self.player_one_bullets)

        for bullet in self.player_two_bullets:
            bullet.move(False)

            if usefull_func.is_collide(bullet, self.player_one):
                self.player_one.health -= 1
                bullet.delete(self.player_two_bullets)

            if bullet.position.x < 0 or bullet.position.x > WIDTH or bullet.position.y < 0 or bullet.position.y > HEIGHT:
                bullet.delete(self.player_two_bullets)
        
        if usefull_func.is_collide(self.player_one, self.player_two) and usefull_func.is_collide(self.player_two, self.player_one):
            self.player_one.health -= 1
            self.player_two.health -= 1
     
        if self.player_one.health < 0 or self.player_two.health < 0:
            game_over = GameOver()
            game_over.run()
            self.game_run = False
                
        # player can't out of window
        self.player_one.line_limit(WIDTH, HEIGHT)
        self.player_two.line_limit(WIDTH, HEIGHT)

    def update(self):
        self.players.update()

        self.player_one_hb.update(self.player_one.health)
        self.player_two_hb.update(self.player_two.health)

    def draw(self):
        WINDOW.blit(self.background, (0, 0))

        for bullet in self.player_one_bullets:
            bullet.draw(WINDOW)

        for bullet in self.player_two_bullets:
            bullet.draw(WINDOW)

        self.players.draw(WINDOW)

        self.player_one_hb.draw(WINDOW)
        self.player_two_hb.draw(WINDOW)
            
    def run(self):
        while self.game_run:
            clock.tick(FPS)

            self.input_handle()

            self.logic()

            self.update()
            
            self.draw()
            
            pygame.display.update()

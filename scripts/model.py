import pygame

import usefull_func


class Player(pygame.sprite.Sprite):
    def __init__(self, image, width, height, position, rotation):
        super().__init__()
        self.image = usefull_func.load_image(image, width, height, rotation)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=position)
        self.position = pygame.math.Vector2(position)
        self.direction = pygame.math.Vector2(0, 1)
        self.speed = 0
        self.angle_speed = 0
        self.angle = 0
        self.health = 100

    def keydown_movement(self, event, keys):
        if event.key == keys[0]:
            self.speed -= 1
        elif event.key == keys[1]:
            self.speed += 1
        elif event.key == keys[2]:
            self.angle_speed = -4
        elif event.key == keys[3]:
            self.angle_speed = 4

    def keyup_movement(self, event, turn):
        if event.key in turn:
            self.angle_speed = 0

    def line_limit(self, window_width, window_height):
        limit = 10
        if self.position.x < 0 + limit:
            self.position.x += 2
        elif self.position.x > window_width - limit:
            self.position.x -= 2

        if self.position.y < 0 + limit:
            self.position.y += 2
        elif self.position.y > window_height - limit:
            self.position.y -= 2

        if ((self.position.x < 0 + limit) or (self.position.x > window_width - limit)
            or (self.position.y < 0 + limit) or (self.position.y > window_height - limit)):
            self.speed = 0

    def update(self):
        if self.angle_speed != 0:
            self.direction.rotate_ip(self.angle_speed)
            self.angle += self.angle_speed
            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        self.position += self.direction * self.speed
        self.rect.center = self.position


class Bullet:
    def __init__(self, image, width, height, position, direction):
        self.image = usefull_func.load_image(image, width, height, 0)
        self.x = position[0]-6
        self.y = position[1]-2
        self.position = pygame.math.Vector2((self.x, self.y))
        self.rect = self.image.get_rect(center=position)
        self.direction = -direction
        self.speed = 5

    def delete(self, bullets):
        bullets.remove(self)

    def draw(self, window):
        window.blit(self.image, self.position)

    def move(self, forward=True):
        if forward:
            self.position += self.direction * self.speed
        elif not forward:
            self.position -= self.direction * self.speed
            
        self.rect.center = self.position


class Bar:
    def __init__(self, image, color, width, height, position):
        self.bar_image_width = width*2
        self.bar_image_height = height*2
        self.bar_image_position = pygame.math.Vector2((position[0]-50, position[1]-5))
        self.image = usefull_func.load_image(image, self.bar_image_width, self.bar_image_height, 0)
        self.position = pygame.math.Vector2(position)
        self.color = color
        self.rect = pygame.Rect(self.position, (width, height))

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.image, self.bar_image_position)

    def update(self, new_value):
        self.rect.width = new_value


class FontCustom:
    def __init__(self, text, size, color, position, font="../Assets/ARCADECLASSIC.ttf"):
        font = pygame.font.Font(font, size)
        self.text = font.render(text, True, color)
        self.position = pygame.math.Vector2(position)

    def draw(self, window):
        window.blit(self.text, self.position)


class Button:
    def __init__(self, text, text_color, button_color, position):
        self.position = pygame.math.Vector2(position)
        self.rect = pygame.Rect(self.position, (200, 100))
        self.button_color = button_color
        # so that the text is really in the middle of the button
        self.text_pos = (self.rect.centerx-35, self.rect.centery-15)
        self.text = FontCustom(text, 32, text_color, self.text_pos)
    
    def draw(self, window):
        pygame.draw.rect(window, self.button_color, self.rect)
        self.text.draw(window)

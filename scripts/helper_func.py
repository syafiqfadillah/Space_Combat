import os 

import pygame


def load_image(load, width, height, rotation, folder="Assets"):
    load = pygame.image.load(os.path.join(folder, load))
    new_scale = pygame.transform.scale(load, (width, height))
    image = pygame.transform.rotate(new_scale, rotation)

    return image


def is_collide(player, other):
    return player.rect.colliderect(other.rect)

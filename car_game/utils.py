import os
import fnmatch

import pygame


def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)


def get_files_with_prefix(directory, prefix) -> list[str]:
    matching_files = []
    for root, _, files in os.walk(directory):
        for filename in fnmatch.filter(files, f"{prefix}*"):
            matching_files.append(os.path.join(root, filename))
    return matching_files

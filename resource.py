import os
import random
import pygame
from buffalo import utils

class Resource:
    def __init__(self,
                 Container=None,
                 resource_type=None,
                 image_path=None,
                 bounds=None,
                 pos=None,
                 _map_=None,
                 worth=1):
        if resource_type is None:
            print("You must specify a resource type.")
            raise ValueError
        else:
            self.rtype = resource_type
        if _map_ is None:
            print("You must specify a map.")
            raise ValueError
        if image_path is None:
            possible_images = next(os.walk(os.path.join("assets", self.rtype)))[2]
            choice = "test.jpg" # don't use jpgs
            while possible_images and (not choice[-4:] == ".png"):
                choice = random.choice(possible_images)
                possible_images.remove(choice)
            self.image_name = choice
            self.image_path = os.path.join("assets", self.rtype, self.image_name)
        else:
            self.image_path = image_path
        self.worth = worth
        self.container = Container
        self.render(self.container)
        if bounds is None and pos is None:
            print("You must specify bounds or pos.")
            raise ValueError
        if pos is None:
            w, h = bounds
            _, __, sw, sh = self.surface.get_rect()
            while True:
                self.pos = (random.randint(0, w - 1), random.randint(0, h - 1))
                x, y = self.pos
                test_pos = x + int(sw / 2), y + sh
                if not _map_.on_water(test_pos) and not _map_.on_stone(test_pos):
                    break
        else:
            self.pos = pos
        #self.render(self.container, depleted=True)

    def blit(self, dest):
        dest.blit(self.surface, self.pos)

    def render(self, Container=None, depleted=False):
        # Container should be the class (itself) that subclasses Resource
        if Container is None:
            print("You must specify a container.")
            raise ValueError
        suffix = "_depleted" if depleted else ""
        try:
            index_of_dot = len(self.image_name) - \
                           self.image_name[::-1].index(".") - 1
        except ValueError:
            print("Invalid image '{}'.".format(self.image_path))
            raise ValueError
        else:
            name = self.image_name[:index_of_dot] + suffix + \
                   self.image_name[index_of_dot:]
        if hasattr(Container, name):
            self.surface = getattr(Container, name)
        else:
            setattr(Container, name,
                    pygame.image.load(self.image_path))
            self.surface = getattr(Container, self.image_name)

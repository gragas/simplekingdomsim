import os
import sys
import pygame
from buffalo import utils
from buffalo.button import Button
from buffalo.input import Input
from buffalo.label import Label
from buffalo.scene import Scene
import menu
import _map

class Profile_Creation(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.BACKGROUND_COLOR = (0, 0, 50, 255)
        Button.DEFAULT_FONT = "default18"
        Label.DEFAULT_FONT = "default24"
        Input.DEFAULT_FONT = "default24"
        self.menu_logo = pygame.image.load(
            os.path.join("assets", "menu_logo_soft_shadow.png"))
        map_width = int(utils.SCREEN_W / _map.Map.TILE_SIZE) + 1
        map_height = int(utils.SCREEN_H / _map.Map.TILE_SIZE) + 1
        map_size = map_width, map_height
        self.m = _map.Map(size=map_size)
        self.labels.add(
            Label(
                (utils.SCREEN_M[0], utils.SCREEN_M[1] + 70),
                "What is your name?",
                x_centered=True,
            )
        )
        self.profile_name_input = Input(
            (utils.SCREEN_M[0], utils.SCREEN_M[1] + 120),
            "Tom",
            x_centered=True,
        )
        self.inputs.add(self.profile_name_input)

        def go_to_main_menu():
            if self.profile_name_input.label.text:
                if self.profile_name_input.label.text[-1] == "|":
                    profile_name = self.profile_name_input.label.text[:-1]
                else:
                    profile_name = self.profile_name_input.label.text
                utils.set_scene(menu.Menu(profile_name, load=False))

        self.buttons.add(
            Button(
                (utils.SCREEN_M[0], utils.SCREEN_M[1] + 170),
                "Continue",
                x_centered=True,
                func=go_to_main_menu,
            )
        )

    def update(self):
        pass

    def blit(self):
        self.m.blit(utils.screen)
        utils.screen.blit(
            self.menu_logo,
            (utils.SCREEN_M[0] - int(728 / 2), utils.SCREEN_M[1] - 70),
        )

    def on_escape(self):
        sys.exit()

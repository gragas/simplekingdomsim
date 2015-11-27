import os
import sys
import pygame
from buffalo import utils
from buffalo.button import Button
from buffalo.input import Input
from buffalo.label import Label
from buffalo.option import Option
from buffalo.scene import Scene
import menu
import profile_creation
import _map

class Profile_Selection(Scene):
    def __init__(self, profile=None):
        Scene.__init__(self)
        self.passed_profile = profile
        self.BACKGROUND_COLOR = (0, 0, 50, 255)
        Button.DEFAULT_FONT = "default18"
        Label.DEFAULT_FONT = "default24"
        Input.DEFAULT_FONT = "default24"
        Option.DEFAULT_FONT = "default24"
        self.menu_logo = pygame.image.load(
            os.path.join("assets", "menu_logo_soft_shadow.png"))
        map_width = int(utils.SCREEN_W / _map.Map.TILE_SIZE) + 1
        map_height = int(utils.SCREEN_H / _map.Map.TILE_SIZE) + 1
        map_size = map_width, map_height
        self.m = _map.Map(size=map_size)

        profiles = next(os.walk("profiles"))[2]

        self.profile_option = Option(
            (utils.SCREEN_M[0], utils.SCREEN_M[1] + 70),
            profiles,
            x_centered=True,
        )
        self.options.add(self.profile_option)

        def go_to_main_menu():
            utils.set_scene(menu.Menu(
                profile_name=self.profile_option.label.text, load=True
            ))

        self.buttons.add(
            Button(
                (utils.SCREEN_M[0], utils.SCREEN_M[1] + 140),
                "Select Profile",
                x_centered=True,
                func=go_to_main_menu,
            )
        )

        def go_to_profile_creation():
            utils.set_scene(profile_creation.Profile_Creation())

        self.buttons.add(
            Button(
                (utils.SCREEN_M[0], utils.SCREEN_M[1] + 210),
                "Create New Profile",
                x_centered=True,
                func=go_to_profile_creation,
            )
        )

        if self.passed_profile is not None:
            self.buttons.add(
                Button(
                    (10, utils.SCREEN_H - 10),
                    "Back",
                    func=self.go_back,
                    invert_y_pos=True,
                )
            )

    def go_back(self):
        utils.set_scene(menu.Menu(profile=self.passed_profile))

    def update(self):
        pass

    def blit(self):
        self.m.blit(utils.screen)
        utils.screen.blit(
            self.menu_logo,
            (utils.SCREEN_M[0] - int(728 / 2), utils.SCREEN_M[1] - 70),
        )

    def on_escape(self):
        if self.passed_profile is not None:
            self.go_back()
        else:
            sys.exit()

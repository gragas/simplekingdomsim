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

class Profile_Selection(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.BACKGROUND_COLOR = (0, 0, 50, 255)
        Button.DEFAULT_FONT = "default18"
        Label.DEFAULT_FONT = "default24"
        Input.DEFAULT_FONT = "default24"
        self.menu_logo = pygame.image.load(os.path.join("assets", "menu_logo.png"))

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

    def update(self):
        pass

    def blit(self):
        utils.screen.blit(
            self.menu_logo,
            (utils.SCREEN_M[0] - int(728 / 2), utils.SCREEN_M[1] - 70),
        )


    def on_escape(self):
        sys.exit()

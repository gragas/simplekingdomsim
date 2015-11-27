import os
import sys
import pygame
from buffalo import utils
from buffalo.button import Button
from buffalo.label import Label
from buffalo.scene import Scene
import _profile
import stats_and_acheivements
import profile_selection
import _map
import new_game

class Menu(Scene):
    def __init__(self, profile_name=None, load=False, profile=None):
        Scene.__init__(self)
        if profile_name is None and profile is None:
            print("ERROR: You must specify a profile to play the game.")
            sys.exit()
        if profile is None:
            self.profile = _profile.Profile(name=profile_name, load_from_file=load)
        else:
            self.profile = profile
        self.profile.save()
        self.BACKGROUND_COLOR = (0, 0, 50, 255)
        Button.DEFAULT_FONT = "default18"
        Label.DEFAULT_FONT = "default48"
        self.menu_logo = pygame.image.load(
            os.path.join("assets", "menu_logo_soft_shadow.png"))
        map_width = int(utils.SCREEN_W / _map.Map.TILE_SIZE) + 1
        map_height = int(utils.SCREEN_H / _map.Map.TILE_SIZE) + 1
        map_size = map_width, map_height
        self.m = _map.Map(size=map_size)

        def go_to_new_game():
            utils.set_scene(new_game.New_Game(self.profile))

        self.buttons.add(
            Button(
                (utils.SCREEN_M[0] - 10, utils.SCREEN_M[1] + 70),
                "New Game",
                invert_x_pos=True,
                func=go_to_new_game,
            )
        )

        def go_to_stats_and_acheivements():
            utils.set_scene(
                stats_and_acheivements.Stats_And_Acheivements(self.profile)
            )

        self.buttons.add(
            Button(
                (utils.SCREEN_M[0], utils.SCREEN_M[1] + 210),
                "Stats and Acheivements",
                x_centered=True,
                func=go_to_stats_and_acheivements,
            )
        )
        self.buttons.add(
            Button(
                (utils.SCREEN_M[0] + 10, utils.SCREEN_M[1] + 70),
                "Load Game",
            )
        )
        self.buttons.add(
            Button(
                (utils.SCREEN_M[0] - 10, utils.SCREEN_M[1] + 140),
                "New Campaign",
                invert_x_pos=True,
            )
        )
        self.buttons.add(
            Button(
                (utils.SCREEN_M[0] + 10, utils.SCREEN_M[1] + 140),
                "Load Campaign",
            )
        )
        
        def go_to_profile_selection():
            utils.set_scene(profile_selection.Profile_Selection(self.profile))

        self.buttons.add(
            Button(
                (utils.SCREEN_M[0], utils.SCREEN_M[1] + 280),
                "Select Profile",
                x_centered=True,
                func=go_to_profile_selection,
            )
        )
        self.buttons.add(
            Button(
                (utils.SCREEN_M[0], utils.SCREEN_M[1] + 350),
                "Settings",
                x_centered=True,
            )
        )
        self.buttons.add(
            Button(
                (utils.SCREEN_M[0], utils.SCREEN_M[1] + 420),
                "Exit",
                x_centered=True,
                func=sys.exit,
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

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
import _map
import game

class New_Game(Scene):
    def __init__(self, passed_profile):
        Scene.__init__(self)
        if passed_profile is None:
            print("You must specify a profile to create a new game.")
            raise RuntimeError
        else:
            self.passed_profile = passed_profile
        self.BACKGROUND_COLOR = (0, 0, 50, 255)
        Button.DEFAULT_FONT = "default18"
        Label.DEFAULT_FONT = "default24"
        Option.DEFAULT_FONT = "default24"
        map_width = int(utils.SCREEN_W / _map.Map.TILE_SIZE) + 1
        map_height = int(utils.SCREEN_H / _map.Map.TILE_SIZE) + 1
        map_size = map_width, map_height
        self.m = _map.Map(size=map_size)
        map_size_label = Label(
            (10, 10),
            "Map Size:"
        )
        self.labels.add(map_size_label)
        multiplayer_label = Label(
            (
                10,
                map_size_label.pos[1] + \
                map_size_label.surface.get_rect()[3] + 10
            ),
            "Multiplayer:"
        )
        self.labels.add(multiplayer_label)
        game_speed_label = Label(
            (
                10,
                multiplayer_label.pos[1] + \
                multiplayer_label.surface.get_rect()[3] + 10
            ),
            "Game Speed:"
        )
        self.labels.add(game_speed_label)
        advanced_map_customization_label = Label(
            (
                10,
                game_speed_label.pos[1] + \
                game_speed_label.surface.get_rect()[3] + 35
            ),
            "Advanced Map Customization"
        )
        self.labels.add(advanced_map_customization_label)
        advmc_separator_label = Label(
            (
                10,
                advanced_map_customization_label.pos[1] + 10
            ),
            "_"*(len("Advanced Map Customization") - 0)
        )
        self.labels.add(advmc_separator_label)
        temperature_volatility_label = Label(
            (
                10,
                advmc_separator_label.pos[1] + \
                advmc_separator_label.surface.get_rect()[3] + 10
            ),
            "Temperature Volatility:"
        )
        self.labels.add(temperature_volatility_label)
        humidity_volatility_label = Label(
            (
                10,
                temperature_volatility_label.pos[1] + \
                temperature_volatility_label.surface.get_rect()[3] + 10
            ),
            "Humidity Volatility:"
        )
        self.labels.add(humidity_volatility_label)
        altitude_volatility_label = Label(
            (
                10,
                humidity_volatility_label.pos[1] + \
                humidity_volatility_label.surface.get_rect()[3] + 10
            ),
            "Altitude Volatility:"
        )
        self.labels.add(altitude_volatility_label)
        
        self.map_size_option = Option(
            (
                game_speed_label.pos[0] + \
                game_speed_label.surface.get_rect()[2] + 10,
                map_size_label.pos[1],
            ),
            ("Medium", "Large", "Humongous", "Tiny", "Small"),
        )
        self.options.add(self.map_size_option)
        self.multiplayer_option = Option(
            (
                game_speed_label.pos[0] + \
                game_speed_label.surface.get_rect()[2] + 10,
                multiplayer_label.pos[1],
            ),
            ("False", "True"),
        )
        self.options.add(self.multiplayer_option)
        self.game_speed_option = Option(
            (
                game_speed_label.pos[0] + \
                game_speed_label.surface.get_rect()[2] + 10,
                game_speed_label.pos[1],
            ),
            ("Normal", "Fast", "Ludicrous Speed", "Marathon", "Slow"),
        )
        self.options.add(self.game_speed_option)

        self.temperature_volatility_option = Option(
            (
                temperature_volatility_label.pos[0] + \
                temperature_volatility_label.surface.get_rect()[2] + 10,
                temperature_volatility_label.pos[1],
            ),
            ("Normal", "High", "Ludicrous", "Essentially None", "Some",),
        )
        self.options.add(self.temperature_volatility_option)
        self.humidity_volatility_option = Option(
            (
                temperature_volatility_label.pos[0] + \
                temperature_volatility_label.surface.get_rect()[2] + 10,
                humidity_volatility_label.pos[1],
            ),
            ("Normal", "High", "Ludicrous", "Essentially None", "Some",),
        )
        self.options.add(self.humidity_volatility_option)
        self.altitude_volatility_option = Option(
            (
                temperature_volatility_label.pos[0] + \
                temperature_volatility_label.surface.get_rect()[2] + 10,
                altitude_volatility_label.pos[1],
            ),
            ("Normal", "High", "Ludicrous", "Essentially None", "Some",),
        )
        self.options.add(self.altitude_volatility_option)

        self.buttons.add(
            Button(
                (10, utils.SCREEN_H - 10),
                "Back",
                invert_y_pos=True,
                func=self.go_back_to_main_menu,
            )
        )
        self.buttons.add(
            Button(
                (utils.SCREEN_W - 10, utils.SCREEN_H - 10),
                "Start",
                invert_y_pos=True,
                invert_x_pos=True,
                func=self.go_to_in_game,
            )
        )

    def go_to_in_game(self):
        self.passed_profile.games_started += 1
        self.passed_profile.save()
        utils.set_scene(
            game.Game(
                profile=self.passed_profile,
                multiplayer=self.multiplayer_option.label.text,
                map_size=self.map_size_option.label.text,
                game_speed=self.game_speed_option.label.text,
                temperature_volatility=self.temperature_volatility_option.label.text,
                humidity_volatility=self.humidity_volatility_option.label.text,
                altitude_volatility=self.altitude_volatility_option.label.text,
            )
        )

    def go_back_to_main_menu(self):
        utils.set_scene(menu.Menu(profile=self.passed_profile))

    def update(self):
        pass

    def blit(self):
        self.m.blit(utils.screen)

    def on_escape(self):
        self.go_back_to_main_menu()

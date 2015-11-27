import sys
import types
from buffalo import utils
from buffalo.button import Button
from buffalo.input import Input
from buffalo.label import Label
from buffalo.scene import Scene
import menu
import _map

class Stats_And_Acheivements(Scene):
    def __init__(self, profile=None):
        Scene.__init__(self)
        self.passed_profile = profile
        if self.passed_profile is None:
            print("You must specify a profile to display the stats " + \
                  "and acheivements of.")
            sys.exit()
        self.BACKGROUND_COLOR = (0, 0, 50, 255)
        Button.DEFAULT_FONT = "default18"
        Label.DEFAULT_FONT = "default18"
        map_width = int(utils.SCREEN_W / _map.Map.TILE_SIZE) + 1
        map_height = int(utils.SCREEN_H / _map.Map.TILE_SIZE) + 1
        map_size = map_width, map_height
        self.m = _map.Map(size=map_size)
        self.buttons.add(
            Button(
                (10, utils.SCREEN_H - 10),
                "Back",
                func=self.go_to_main_menu,
                invert_y_pos=True,
            )
        )

        attrs = [attr for attr in dir(profile) if not attr.startswith("__")]
        # Get all non-builtin attributes
        attrs = filter(lambda x: not "__call__" in dir(getattr(profile, x)), attrs)
        # Remove all the methods
        attrs = list(attrs)
        # Turn attrs back into a list
        attrs[attrs.index("name")], attrs[0] = attrs[0], attrs[attrs.index("name")]
        # Put profile.name at the front of the list
        attrs[attrs.index("level")], attrs[1] = (
            attrs[1], attrs[attrs.index("level")]
        )
        # Put profile.level second to the front of the list
        attrs[2:] = sorted(attrs[2:])
        # Sort the rest of the list lexicographically
        for indx, attr in enumerate(attrs):
            if not attr == "date_created":
                value = str(getattr(profile, attr))
            else:
                value = profile.date_created.strftime("%Y-%m-%d")
            string = attr.replace("_", " ").title() + ": " + value
            self.labels.add(Label((10, 10 + indx * 25),string,))

    def go_to_main_menu(self):
        utils.set_scene(menu.Menu(profile=self.passed_profile))

    def update(self):
        pass

    def blit(self):
        self.m.blit(utils.screen)

    def on_escape(self):
        self.go_to_main_menu()

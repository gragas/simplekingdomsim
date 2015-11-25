import sys
import types
from buffalo import utils
from buffalo.button import Button
from buffalo.input import Input
from buffalo.label import Label
from buffalo.scene import Scene
import menu

class Stats_And_Acheivements(Scene):
    def __init__(self, profile=None):
        Scene.__init__(self)
        if profile is None:
            print("You must specify a profile to display the stats " + \
                  "and acheivements of.")
            sys.exit()
        self.BACKGROUND_COLOR = (0, 0, 50, 255)
        Button.DEFAULT_FONT = "default18"
        Label.DEFAULT_FONT = "default18"

        def go_to_main_menu():
            utils.set_scene(menu.Menu(profile=profile))

        self.buttons.add(
            Button(
                (10, utils.SCREEN_H - 10),
                "Back",
                func=go_to_main_menu,
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

    def update(self):
        pass

    def blit(self):
        pass

    def on_escape(self):
        sys.exit()

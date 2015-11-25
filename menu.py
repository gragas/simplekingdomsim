import sys
from buffalo import utils
from buffalo.button import Button
from buffalo.label import Label
from buffalo.scene import Scene

class Menu(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.BACKGROUND_COLOR = (0, 0, 50, 255)
        Button.DEFAULT_FONT = "default18"
        Label.DEFAULT_FONT = "default48"
        self.labels.add(
            Label(
                (utils.SCREEN_M[0], utils.SCREEN_M[1] - 70),
                "SIMPLE KINGDOM SIM",
                x_centered=True,
            )
        )
        self.buttons.add(
            Button(
                (utils.SCREEN_M[0], utils.SCREEN_M[1] + 150),
                "New Game",
                x_centered=True,
            )
        )
        self.buttons.add(
            Button(
                (utils.SCREEN_M[0], utils.SCREEN_M[1] + 220),
                "Exit",
                x_centered=True,
                func=sys.exit,
            )
        )

    def update(self):
        pass

    def blit(self):
        pass

    def on_escape(self):
        sys.exit()

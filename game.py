import sys
import pygame
from buffalo import utils
from buffalo.scene import Scene
import _map

class _Helper:
    @staticmethod
    def initialize(fPos=(0, 0), speed=0.125):
        _Helper.fPos = fPos
        _Helper.speed = speed

    @staticmethod
    def pos():
        x, y = _Helper.fPos
        return (int(x), int(y))

    @staticmethod
    def update():
        _Helper.xv, _Helper.yv = 0.0, 0.0
        keys = pygame.key.get_pressed()
        speed = _Helper.speed * utils.delta
        if keys[pygame.K_LSHIFT]:
            speed *= 2.0
        if keys[pygame.K_w]:
            _Helper.yv -= speed
        if keys[pygame.K_s]:
            _Helper.yv += speed
        if keys[pygame.K_d]:
            _Helper.xv += speed
        if keys[pygame.K_a]:
            _Helper.xv -= speed
        x, y = _Helper.fPos
        x += _Helper.xv
        y += _Helper.yv
        _Helper.fPos = x, y

class Game(Scene):
    def __init__(self,
                 profile=None,
                 multiplayer=None,
                 map_size=None,
                 game_speed=None,
                 temperature_volatility=None,
                 humidity_volatility=None,
                 altitude_volatility=None,):
        Scene.__init__(self)
        self.BACKGROUND_COLOR = (0, 0, 50, 255)
        if profile is None:
            print("You must specify a profile to play this game with.")
            raise RuntimeError
        else:
            self.profile = profile
        if multiplayer is None:
            print("You must specify whether this game is multiplayer.")
            raise RuntimeError
        else:
            if multiplayer == "True":
                self.multiplayer = True
            elif multiplayer == "False":
                self.multiplayer = False
            else:
                print(
                    "{} is not a valid multiplayer state.".format(str(multiplayer)))
                raise RuntimeError
        if map_size is None:
            print("You must specify the map size.")
            raise RuntimeError
        else:
            if map_size == "Tiny":
                self.map_size = (30, 30)
            elif map_size == "Small":
                self.map_size = (75, 75)
            elif map_size == "Medium":
                self.map_size = (100, 100)
            elif map_size == "Large":
                self.map_size = (150, 150)
            elif map_size == "Humongous":
                self.map_size = (200, 200)
            else:
                print("{} is not a valid map size.".format(str(map_size)))
                raise RuntimeError
        if game_speed is None:
            print("You must specify the game speed.")
            raise RuntimeError
        else:
            if game_speed == "Marathon":
                self.game_speed = 1
            elif game_speed == "Slow":
                self.game_speed = 2
            elif game_speed == "Normal":
                self.game_speed = 3
            elif game_speed == "Fast":
                self.game_speed = 5
            elif game_speed == "Ludicrous Speed":
                self.game_speed = 10
            else:
                print("{} is not a valid game speed.".format(str(game_speed)))
                raise RuntimeError
        if temperature_volatility is not None:
            if temperature_volatility == "Essentially None":
                self.temperature_volatility = (1, 0)
            elif temperature_volatility == "Some":
                self.temperature_volatility = (3, 0)
            elif temperature_volatility == "Normal":
                self.temperature_volatility = (5, 0)
            elif temperature_volatility == "High":
                self.temperature_volatility = (7, 1)
            elif temperature_volatility == "Ludicrous":
                self.temperature_volatility = (10, 2)
        else:
            self.temperature_volatility = (None, None)
        if humidity_volatility is not None:
            if humidity_volatility == "Essentially None":
                self.humidity_volatility = (1, 0)
            elif humidity_volatility == "Some":
                self.humidity_volatility = (3, 0)
            elif humidity_volatility == "Normal":
                self.humidity_volatility = (5, 0)
            elif humidity_volatility == "High":
                self.humidity_volatility = (7, 1)
            elif humidity_volatility == "Ludicrous":
                self.humidity_volatility = (10, 2)
        else:
            self.humidity_volatility = (None, None)
        if altitude_volatility is not None:
            if altitude_volatility == "Essentially None":
                self.altitude_volatility = (1, 0)
            elif altitude_volatility == "Some":
                self.altitude_volatility = (3, 0)
            elif altitude_volatility == "Normal":
                self.altitude_volatility = (5, 0)
            elif altitude_volatility == "High":
                self.altitude_volatility = (7, 1)
            elif altitude_volatility == "Ludicrous":
                self.altitude_volatility = (10, 2)
        else:
            self.altitude_volatility = (None, None)
        mdt, odt = self.temperature_volatility
        mdh, odh = self.humidity_volatility
        mda, oda = self.altitude_volatility
        self.m = _map.Map(size=self.map_size,
                          i_temp=None, max_d_temp=mdt, off_d_temp=odt,
                          i_hum=None, max_d_hum=mdh, off_d_hum=odh,
                          i_alt=None, max_d_alt=mda, off_d_alt=oda,
        )
        _Helper.initialize()

    def blit(self):
        x, y = _Helper.pos()
        self.m.blit(utils.screen, pos=(-x, -y))

    def update(self):
        _Helper.update()

    def on_escape(self):
        sys.exit()

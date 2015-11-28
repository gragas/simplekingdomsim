import functools
import random
import sys
import pygame
from buffalo import utils
from buffalo.scene import Scene
import wood, stone

class Map:

    TILE_SIZE = 32

    def __init__(self, size=(60, 34),
                 i_temp=None, max_d_temp=5, off_d_temp=0,
                 i_hum=None, max_d_hum=5, off_d_hum=0,
                 i_alt=None, max_d_alt=5, off_d_alt=0,
                 wood_density=10, stone_density=0.25):
        # size is a 2-tuple representing the width
        # and height of the map in tiles
        self.size = self.width, self.height = size
        # i_* is the initial value of attribute *
        # max_d_* is the maximum delta of attribute *
        self.i_temp = i_temp if i_temp is not None else random.randint(50, 90)
        self.max_d_temp = max_d_temp
        self.off_d_temp = off_d_temp
        self.temp_arr = functools.reduce(
            lambda x, y: x + y,
            [[i + self.off_d_temp]*(self.max_d_temp - i) for i in range(self.max_d_temp)]
        ) # e.g., [0, 0, 0, 0, 1, 1, 1, 2, 2, 3]
        self.temp_arr = self.temp_arr + [-i for i in self.temp_arr]
        self.i_hum = i_hum if i_hum is not None else random.randint(10, 50)
        self.max_d_hum = max_d_hum
        self.off_d_hum = off_d_hum
        self.hum_arr = functools.reduce(
            lambda x, y: x + y,
            [[i + self.off_d_hum]*(self.max_d_hum - i) for i in range(self.max_d_hum)]
        ) # e.g., [0, 0, 0, 0, 1, 1, 1, 2, 2, 3]
        self.hum_arr = self.hum_arr + [-i for i in self.hum_arr]
        self.i_alt = i_alt if i_alt is not None else random.randint(0, 200)
        self.max_d_alt = max_d_alt
        self.off_d_alt = off_d_alt
        self.alt_arr = functools.reduce(
            lambda x, y: x + y,
            [[i + self.off_d_alt]*(self.max_d_alt - i) for i in range(self.max_d_alt)]
        ) # e.g., [0, 0, 0, 0, 1, 1, 1, 2, 2, 3]
        self.alt_arr = self.alt_arr + [-i for i in self.alt_arr]
        self.tiles = dict()
        self.surface = utils.empty_surface((self.width * Map.TILE_SIZE, self.height * Map.TILE_SIZE))
        self.wood_density = wood_density
        self.stone_density = stone_density
        self.water_tiles = set()
        self.generate_map()
        self.render()

    def generate_map(self):
        self.tiles[(0, 0)] = (self.i_temp, self.i_hum, self.i_alt)
        edge_tiles = [(0, 0)]
        while len(self.tiles) < (self.width * self.height):
            while edge_tiles:
                (x, y) = random.choice(edge_tiles)
                for y_offset in range(-1, 2):
                    for x_offset in range(-1, 2):
                        x_cand, y_cand = x + x_offset, y + y_offset
                        if ((x_cand, y_cand) not in self.tiles) and \
                           (x_cand >= 0 and x_cand < self.width) and \
                           (y_cand >= 0 and y_cand < self.height):
                           edge_tiles.append((x_cand, y_cand))
                           temp, hum, alt = self.tiles[(x, y)]
                           self.tiles[(x_cand, y_cand)] = (
                               temp + random.choice(self.temp_arr),
                               hum + random.choice(self.hum_arr),
                               alt + random.choice(self.alt_arr),
                           )
                edge_tiles.remove((x, y))
        self.resources = set()
        self.render()
        total_tiles = self.width * self.height
        self.stone_tiles = set()
        total_stone = int(total_tiles * self.stone_density / 100)
        for _ in range(total_stone):
            self.resources.add(
                stone.Stone(
                    bounds=(
                        self.width * Map.TILE_SIZE,
                        self.height * Map.TILE_SIZE
                    ),
                    _map_=self,
                )
            )
        total_wood = int(total_tiles * self.wood_density / 100)
        for _ in range(total_wood):
            self.resources.add(
                wood.Wood(
                    bounds=(
                        self.width * Map.TILE_SIZE,
                        self.height * Map.TILE_SIZE
                    ),
                    _map_=self,
                )
            )

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                temp, hum, alt = self.tiles[(x, y)]
                tmod = int(temp / 70.0 * 150)
                r = tmod
                g = tmod + int(abs(temp - 70) / 30.0 * 200)
                b = tmod + int(hum / 100.0 * 200)
                if r > 255: r = 255
                if r < 0: r = 0
                if g > 255: g = 255
                if g < 0: g = 0
                if b > 255: b = 255
                if b < 0: b = 0
                if r < 200 and g < 200:
                    r = int(0.15 * r)
                    g = int(0.15 * g)
                    b = min((255, int(1.0125 * b)))
                    self.water_tiles.add((x, y))
                else:
                    r = int(0.95 * r)
                    g = int(0.85 * g)
                    b = int(0.75 * b)
                color = (r, g, b, 255)
                self.surface.fill(
                    color,
                    pygame.Rect(
                        x * Map.TILE_SIZE, y * Map.TILE_SIZE,
                        Map.TILE_SIZE, Map.TILE_SIZE
                    )
                )
        for resource in self.resources:
            resource.blit(self.surface)

    def blit(self, dest, pos=(0, 0)):
        dest.blit(self.surface, pos)

    def __str__(self):
        max_tile = max(
            self.tiles,
            key=lambda j: len(str(max(self.tiles.get(j), key=lambda x: len(str(x)))))
        )
        num_chars = len(str(max(self.tiles[max_tile], key=lambda x: len(str(x)))))
        temp_str = list()
        hum_str = list()
        alt_str = list()
        for y in range(self.height):
            temp_row = list()
            hum_row = list()
            alt_row = list()
            for x in range(self.width):
                temp, hum, alt = self.tiles[(x, y)]
                temp_row.append(" "*(num_chars - len(str(temp))) + str(temp))
                hum_row.append(" "*(num_chars - len(str(hum))) + str(hum))
                alt_row.append(" "*(num_chars - len(str(alt))) + str(alt))
            temp_str.append(" ".join(temp_row))
            hum_str.append(" ".join(hum_row))
            alt_str.append(" ".join(alt_row))
        temp_str = "Temperatures:\n" + "\n".join(temp_str)
        hum_str = "Humdities:\n" + "\n".join(hum_str)
        alt_str = "Altitudes:\n" + "\n".join(alt_str)
        return "\n\n".join([temp_str, hum_str, alt_str])

    def on_water(self, pos):
        x, y = pos
        return (int(x / Map.TILE_SIZE), int(y / Map.TILE_SIZE)) in self.water_tiles

    def on_stone(self, pos):
        x, y = pos
        return (int(x / Map.TILE_SIZE), int(y / Map.TILE_SIZE)) in self.stone_tiles

class _MainScene(Scene):
    # This class is only used when __name__ == "__main__"
    # It displays a default map
    def __init__(self):
        Scene.__init__(self)
        self.m = Map()

    def on_escape(self):
        sys.exit()

    def blit(self):
        self.m.blit(utils.screen)

    def update(self):
        pass

def main():
    while not utils.end:
        utils.scene.logic()
        utils.scene.update()
        utils.scene.render()
        utils.delta = utils.clock.tick( utils.FRAMES_PER_SECOND )    

if __name__ == "__main__":
    if not utils.init(caption="Simple Kingdom Simulator", fullscreen=True,):
        print("Buffalo failed to initialize")
        pygame.quit()
        sys.exit()
    utils.set_scene(_MainScene())
    main()
    pygame.quit()

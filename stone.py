import resource
import _map

class Stone(resource.Resource):
    def __init__(self, image_path=None, bounds=None, pos=None, _map_=None):
        resource.Resource.__init__(
            self,
            Container=Stone,
            resource_type="stone",
            bounds=bounds,
            pos=pos,
            _map_=_map_,
            worth=1,
        )
        x, y = self.pos
        cx, cy = int(x / _map.Map.TILE_SIZE), int(y / _map.Map.TILE_SIZE)
        _, __, w, h = self.surface.get_rect()
        cw, ch = int(w / _map.Map.TILE_SIZE), int(h / _map.Map.TILE_SIZE)
        for i in range(cx, cx + cw + 1):
            for j in range(cy + 1, cy + ch + 2):
                _map_.stone_tiles.add((i, j))

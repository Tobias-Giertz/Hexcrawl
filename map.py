import random

from hex import Hex
from roads import RoadNetwork
from noisemap import noise_value
from coordinates import *
from terrain import Terrain

class Map:
    def __init__(self):
        self.hexes = {}
        self.road_network = RoadNetwork()

    def to_dict(self):
        return {
            "hexes": [h.to_dict() for h in self.hexes.values()],
            "road_network": self.road_network.to_dict(),
        }

    @classmethod
    def from_dict(cls, data):
        map = cls()

        for h_data in data["hexes"]:
            hex = Hex.from_dict(h_data)
            map.hexes[(hex.q, hex.r)] = hex

        map.road_network = RoadNetwork.from_dict(data["road_network"], map)

        return map

    def _add_hex(self, q, r, terrain=None):
        hex = Hex(q, r, terrain)
        self.hexes[(q, r)] = hex
        return hex

    def get_hex(self, q, r):
        return self.hexes.get((q, r))
    
    def get_neighbor_coords(self, hex):
        for dq, dr in DIRECTIONS.values():
            yield hex.q + dq, hex.r + dr
    
    def is_edge_hex(self, hex):
        q, r = hex.q, hex.r
        for direction, (dq, dr) in DIRECTIONS.items():
            neighbor = self.get_hex(q + dq, r + dr)
            if neighbor is None:
                return True
        return False

### ===================================================== ###

    def add_hex(self, q:int, r:int, t=None, m="perlin"):
        if t is not None and t not in Terrain:
            raise ValueError(f"Invalid terrain: {t}")

        if t is not None:
            self._add_hex(q, r, t)
        elif m == "perlin":
            self._add_hex_from_noise(q, r)
        elif m == "random":
            self._add_hex_from_random(q, r)
        else:
            raise ValueError(f"Unknown generation method: {m}")

    def _add_hex_from_random(self, q, r):
        seed = random.randint(1, 10)
        if seed < 2:
            terrain = Terrain.SEA
        elif seed < 5:
            terrain = Terrain.PLAINS
        elif seed < 8:
            terrain = Terrain.FOREST
        else:
            terrain = Terrain.MOUNTAIN
        self._add_hex(q, r, terrain)

    def _add_hex_from_noise(self, q, r):
        x, y = axial_to_pixel(q, r)
        noise = noise_value(x, y)
        # print(f'Noise value for ({q}, {r}): {noise}')  # Debug print
        # Use noise value to determine terrain (example logic - adjust as needed)
        if noise < 0.45:
            terrain = Terrain.SEA
        elif noise < 0.52:
            terrain = Terrain.PLAINS
        elif noise < 0.60:
            terrain = Terrain.FOREST
        else:
            terrain = Terrain.MOUNTAIN
        self._add_hex(q, r, terrain)



    def print_map(self):
        if not self.hexes:
            print("(empty map)")
            return

        qs = [q for (q, r) in self.hexes]
        rs = [r for (q, r) in self.hexes]

        min_q, max_q = min(qs), max(qs)
        min_r, max_r = min(rs), max(rs)

        for r in range(min_r, max_r + 1):
            # indent varannan rad (för hex-känsla)
            indent = "  " if r % 2 else ""
            line = indent

            for q in range(min_q, max_q + 1):
                h = self.get_hex(q, r)

                if h is None:
                    line += " . "
                else:
                    line += f"{self._symbol(h)} "

            print(line)

    def _symbol(self, hex):
        if hex.terrain == Terrain.FOREST:
            return "F"
        elif hex.terrain == Terrain.PLAINS:
            return "P"
        elif hex.terrain == Terrain.MOUNTAIN:
            return "M"
        elif hex.terrain == Terrain.SEA:
            return "S"
        else:
            return "?"
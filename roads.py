class Road:
    def __init__(self, hex_a, hex_b):
        self.hexes = frozenset([hex_a, hex_b])

    def to_dict(self):
        h1, h2 = tuple(self.hexes)
        return {
            "a": [h1.q, h1.r],
            "b": [h2.q, h2.r],
        }

    @classmethod
    def from_dict(cls, data, map_obj):
        hex_a = map_obj.get_hex(*data["a"])
        hex_b = map_obj.get_hex(*data["b"])
        return cls(hex_a, hex_b)

    def connects(self, h1, h2):
        return frozenset([h1, h2]) == self.hexes



class RoadNetwork:
    def __init__(self):
        self.roads = {}

    def to_dict(self):
        return {
            "roads": [road.to_dict() for road in self.roads.values()]
        }

    @classmethod
    def from_dict(cls, data, map_obj):
        network = cls()

        for road_data in data["roads"]:
            road = Road.from_dict(road_data, map_obj)
            h1, h2 = tuple(road.hexes)
            key = frozenset([h1, h2])
            network.roads[key] = road

        return network

    def add_road(self, hex_a, hex_b):
        key = frozenset([hex_a, hex_b])
        self.roads[key] = Road(hex_a, hex_b)

    def get_road(self, hex_a, hex_b):
        return self.roads.get(frozenset([hex_a, hex_b]))
from enum import Enum

class Terrain(Enum):
    SEA = "sea"
    ARCHIPELAGO = "archipelago"
    PLAINS = "plains"
    FOREST = "forest"
    MOUNTAIN = "mountain"


TERRAIN_DATA = {
    Terrain.SEA: {
        "treshold": 0.42,
        "map_color": "#0000FF",
        "speed": 8,
        "encounter table": {
            0.0: "nothing",
            0.5: "easy encounter",
            0.8: "medium encounter",
            0.95: "hard encounter"
        }
    },
    Terrain.ARCHIPELAGO: {
        "treshold": 0.46,
        "map_color": "#00CED1",
        "speed": 8,
        "encounter table": {
            0.0: "nothing",
            0.5: "easy encounter",
            0.8: "medium encounter",
            0.95: "hard encounter"
        }
    },
    Terrain.PLAINS: {
        "treshold": 0.52,
        "map_color": "#00A800",
        "speed": 2,
        "encounter table": {
            0.0: "nothing",
            0.5: "easy encounter",
            0.8: "medium encounter",
            0.95: "hard encounter"
        }
    },
    Terrain.FOREST: {
        "treshold": 0.60,
        "map_color": "#0F4D0F",
        "speed": 4,
        "encounter table": {
            0.0: "nothing",
            0.5: "easy encounter",
            0.8: "medium encounter",
            0.95: "hard encounter"
        }
    },
    Terrain.MOUNTAIN: {
        "treshold": 1.0,
        "map_color": "#808080",
        "speed": 8,
        "encounter table": {
            0.0: "nothing",
            0.5: "easy encounter",
            0.8: "medium encounter",
            0.95: "hard encounter"
        }
    },
}
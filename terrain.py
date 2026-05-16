from enum import Enum

class Terrain(Enum):
    PLAINS = "plains"
    FOREST = "forest"
    MOUNTAIN = "mountain"
    SEA = "sea"


TERRAIN_DATA = {
    Terrain.PLAINS: {
        "speed": 2,
    },
    Terrain.FOREST: {
        "speed": 4,
    },
    Terrain.MOUNTAIN: {
        "speed": 8,
    },
    Terrain.SEA: {
        "speed": 8,
    },
}